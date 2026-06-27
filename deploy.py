#!/usr/bin/env python3
"""
Vanguard Technologies - Dedicated Deployment Script (ASCII-Safe Edition)
Automates SSH/SFTP code upload and post-deployment configuration on the production server.
"""

import os
import sys
import hashlib
import json
import argparse
import fnmatch
import time
from pathlib import Path

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False


class DeploymentManager:
    def __init__(self, env_file=None):
        self.project_root = Path.cwd()
        self.hash_file = self.project_root / ".deploy_hashes.json"
        
        # Load configuration from env
        self.load_settings(env_file)
        self.ignored_patterns = self.load_gitignore_patterns()

        print("=" * 50)
        print(f"[Project] {self.project_root.name}")
        print(f"[Server]  {self.server_ip}:{self.ssh_port}")
        print(f"[User]    {self.username}")
        print(f"[Remote]  {self.remote_path}")
        print("=" * 50)

    def load_settings(self, env_file=None):
        """Load SSH and deploy settings from .env file"""
        if env_file is None:
            env_file = self.project_root / ".env"

        # Defaults
        self.server_ip = "84.247.179.163"
        self.username = "vanguard"
        self.ssh_port = "2951"
        self.private_key = "id_rsa"
        self.ssh_key_passphrase = None
        self.remote_path = "/home/vanguard/vanguard_prod"
        self.python_version = "3.11"
        self.django_settings = "config.settings"

        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if key == 'SSH_HOST':
                                self.server_ip = value
                            elif key == 'SSH_PORT':
                                self.ssh_port = value
                            elif key == 'SSH_USER':
                                self.username = value
                            elif key == 'SSH_KEY_PATH':
                                self.private_key = value
                            elif key == 'SSH_PASSPHRASE':
                                self.ssh_key_passphrase = value
                            elif key == 'SSH_REMOTE_PATH':
                                self.remote_path = value
                            elif key == 'PYTHON_VERSION':
                                self.python_version = value
                            elif key == 'DJANGO_SETTINGS_MODULE':
                                self.django_settings = value
            except Exception as e:
                print(f"[Warning] Cannot read .env file: {e}")

    def load_gitignore_patterns(self):
        """Load exclude patterns from .gitignore"""
        patterns = []
        gitignore_path = self.project_root / ".gitignore"
        
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        
        # Add core deployment exclusions
        patterns.extend([
            '__pycache__', '*.pyc', '.deploy_hashes.json', '*.log', 
            'deploy_logs', '.env', 'db.sqlite3', 'deploy.py', 'test_conn.py'
        ])
        return patterns

    def is_ignored(self, file_path):
        """Check if file matches ignore patterns"""
        relative_path = str(file_path.relative_to(self.project_root)).replace('\\', '/')
        
        # Always allow these important deployment files
        important_files = ['.htaccess', 'passenger_wsgi.py']
        if relative_path in important_files:
            return False
        
        # Ignore hidden files in root (except allowed ones)
        parts = relative_path.split('/')
        if parts[0].startswith('.') and parts[0] not in ['.well-known']:
            return True
            
        for pattern in self.ignored_patterns:
            if pattern.startswith('.'):
                continue
            if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(file_path.name, pattern):
                return True
                
        return False

    def get_file_hash(self, file_path):
        """Compute MD5 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None

    def get_all_files(self):
        """Get all local files to deploy"""
        files = []
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and not self.is_ignored(file_path):
                files.append(file_path)
        return files

    def _create_ssh_connection(self):
        """Establish SSH connection using private key"""
        if not PARAMIKO_AVAILABLE:
            raise Exception("Library 'paramiko' is not available. Please run: pip install paramiko")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connect_params = {
            'hostname': self.server_ip,
            'port': int(self.ssh_port),
            'username': self.username,
            'timeout': 30
        }
        
        if self.private_key:
            key_path = Path(self.private_key)
            if not key_path.is_absolute():
                key_path = self.project_root / self.private_key
                
            if key_path.exists():
                try:
                    pkey = paramiko.RSAKey.from_private_key_file(
                        str(key_path), 
                        password=self.ssh_key_passphrase
                    )
                    connect_params['pkey'] = pkey
                except Exception as e:
                    raise Exception(f"Failed to load SSH key: {e}")
            else:
                raise Exception(f"SSH private key file not found at: {key_path}")
        else:
            raise Exception("No SSH Key defined in settings.")
            
        ssh.connect(**connect_params)
        return ssh

    def test_connection(self):
        """Verify SSH connection and remote permissions"""
        print("[Scan] Testing SSH Connection...")
        try:
            ssh = self._create_ssh_connection()
            stdin, stdout, stderr = ssh.exec_command("echo 'connection_successful'")
            result = stdout.read().decode().strip()
            ssh.close()
            
            if result == 'connection_successful':
                print(f"[OK] Connection Successful! ({self.username}@{self.server_ip}:{self.ssh_port})")
                return True
            else:
                print("[Error] Shell command execution failed.")
                return False
        except Exception as e:
            print(f"[Error] Connection Failed: {e}")
            return False

    def get_remote_files_with_stats(self, sftp, remote_path, files_dict, base_path=""):
        """Recursively retrieve list of remote files and their metadata"""
        try:
            for item in sftp.listdir_attr(remote_path):
                if item.filename.startswith('.'):
                    continue
                
                item_path = f"{remote_path}/{item.filename}"
                relative_path = f"{base_path}/{item.filename}" if base_path else item.filename
                
                if item.st_mode and item.st_mode & 0o040000:  # Directory
                    self.get_remote_files_with_stats(sftp, item_path, files_dict, relative_path)
                else:  # File
                    files_dict[relative_path] = {
                        'size': item.st_size,
                        'mtime': int(item.st_mtime)
                    }
        except Exception:
            pass

    def get_modified_files(self):
        """Identify modified or new files by comparing with server"""
        print("[Scan] Scanning local and remote directories...")
        try:
            ssh = self._create_ssh_connection()
            sftp = ssh.open_sftp()
            
            local_files = self.get_all_files()
            local_files_dict = {}
            for file_path in local_files:
                relative_path = str(file_path.relative_to(self.project_root)).replace('\\', '/')
                stat = file_path.stat()
                local_files_dict[relative_path] = {
                    'path': file_path,
                    'size': stat.st_size,
                    'mtime': int(stat.st_mtime)
                }
            
            remote_files_dict = {}
            self.get_remote_files_with_stats(sftp, self.remote_path, remote_files_dict)
            
            modified_files = []
            new_count = 0
            size_diff_count = 0
            
            for relative_path, local_info in local_files_dict.items():
                if relative_path not in remote_files_dict:
                    modified_files.append(local_info['path'])
                    new_count += 1
                else:
                    remote_info = remote_files_dict[relative_path]
                    if local_info['size'] != remote_info['size']:
                        modified_files.append(local_info['path'])
                        size_diff_count += 1
            
            sftp.close()
            ssh.close()
            
            total_modified = len(modified_files)
            if total_modified > 0:
                print(f"[Scan] Found {total_modified} files to upload ({new_count} new, {size_diff_count} modified).")
            else:
                print("[OK] All files are up-to-date on the server.")
                
            return modified_files
        except Exception as e:
            print(f"[Error] Failed scanning remote directory: {e}")
            return []

    def _create_remote_directories(self, sftp, remote_file):
        """Create parent directories recursively on the server if they don't exist"""
        remote_dir = '/'.join(remote_file.split('/')[:-1])
        if remote_dir != self.remote_path:
            path_parts = remote_dir.replace(self.remote_path + '/', '').split('/')
            current_path = self.remote_path
            for part in path_parts:
                if part:
                    current_path = f"{current_path}/{part}"
                    try:
                        sftp.mkdir(current_path)
                    except Exception:
                        pass

    def upload_files(self, files, overwrite_all=False):
        """Upload selected files via SFTP"""
        if not files:
            print("[Info] No files to upload.")
            return True
            
        print(f"[Upload] Uploading {len(files)} files...")
        start_time = time.time()
        uploaded_count = 0
        skipped_count = 0
        
        try:
            ssh = self._create_ssh_connection()
            sftp = ssh.open_sftp()
            
            # Ensure base remote path exists
            try:
                sftp.mkdir(self.remote_path)
            except Exception:
                pass
            
            total_files = len(files)
            for i, file_path in enumerate(files):
                if not file_path.exists():
                    skipped_count += 1
                    continue
                
                relative_path = str(file_path.relative_to(self.project_root)).replace('\\', '/')
                remote_file = f"{self.remote_path}/{relative_path}"
                
                # Check if we should skip
                if not overwrite_all:
                    try:
                        remote_stat = sftp.stat(remote_file)
                        local_stat = file_path.stat()
                        if remote_stat.st_size == local_stat.st_size:
                            skipped_count += 1
                            continue
                    except Exception:
                        pass
                
                # Show progress bar (ASCII only)
                percentage = ((i + 1) / total_files) * 100
                bar = '#' * int(25 * (i + 1) // total_files) + '-' * (25 - int(25 * (i + 1) // total_files))
                print(f"\r[{bar}] {percentage:.1f}% - Uploaded: {uploaded_count}, Skipped: {skipped_count}", end='', flush=True)
                
                try:
                    self._create_remote_directories(sftp, remote_file)
                    sftp.put(str(file_path), remote_file)
                    uploaded_count += 1
                except Exception as e:
                    print(f"\n[Warning] Error uploading {relative_path}: {e}")
            
            print()
            sftp.close()
            ssh.close()
            
            total_time = time.time() - start_time
            print(f"[OK] Upload completed in {total_time:.1f}s - Uploaded: {uploaded_count}, Skipped: {skipped_count}")
            return True
        except Exception as e:
            print(f"\n[Error] SFTP Upload Failed: {e}")
            return False

    def run_post_deploy_commands(self):
        """Execute migrations, static collection, database seeding, and application reload on server"""
        remote_app_name = Path(self.remote_path).name
        venv_python = f"/home/{self.username}/virtualenv/{remote_app_name}/{self.python_version}/bin/python"
        venv_pip = f"/home/{self.username}/virtualenv/{remote_app_name}/{self.python_version}/bin/pip"
        manage_py = f"{self.remote_path}/manage.py"

        commands = [
            (f"{venv_pip} install -r {self.remote_path}/requirements.txt", "Pip Dependencies Install"),
            (f"{venv_python} {manage_py} migrate --noinput", "Database Migrations"),
            (f"{venv_python} {manage_py} collectstatic --noinput", "Collect Static Files"),
            (f"{venv_python} {manage_py} seed_initial_content", "Database Content Seeding"),
            (f"/usr/sbin/cloudlinux-selector restart --json --interpreter python --app-root {remote_app_name}", "Reload Web Application")

        ]

        try:
            ssh = self._create_ssh_connection()
            sftp = ssh.open_sftp()
            try:
                sftp.put(str(self.project_root / ".env"), f"{self.remote_path}/.env")
                print("  [OK] Uploaded .env file to server.")
            except Exception as e:
                print(f"  [Warning] Failed to upload .env: {e}")
            sftp.close()

            print("\n[Config] Running post-deployment configuration on server...")

            
            for cmd, label in commands:
                print(f"  Running: {label}...")
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
                exit_code = stdout.channel.recv_exit_status()
                err = stderr.read().decode().strip()
                
                if exit_code == 0:
                    print(f"  [OK] {label} - Completed successfully.")
                else:
                    print(f"  [Failed] {label} - Failed (Exit Code: {exit_code}).")
                    if err:
                        print(f"     Error output:\n     {err[-500:]}")
            
            ssh.close()
            print("\n[OK] Post-deployment configuration finished!")
        except Exception as e:
            print(f"[Warning] Failed running post-deployment commands: {e}")

    def deploy(self, all_files=False):
        """Main deploy execution"""
        if not self.test_connection():
            return False
            
        if all_files:
            files_to_deploy = self.get_all_files()
        else:
            files_to_deploy = self.get_modified_files()
            
        if not files_to_deploy:
            print("[OK] Production files are already up-to-date.")
            return True
            
        confirm = input(f"Confirm: Do you want to deploy {len(files_to_deploy)} files to production? (y/N): ").lower()
        if confirm != 'y':
            print("[Info] Deployment cancelled.")
            return False
            
        success = self.upload_files(files_to_deploy, overwrite_all=all_files)
        if success:
            # Save hashes locally to optimize future runs
            all_files_list = self.get_all_files()
            current_hashes = {}
            for file_path in all_files_list:
                relative_path = str(file_path.relative_to(self.project_root)).replace('\\', '/')
                current_hashes[relative_path] = self.get_file_hash(file_path)
            
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump(current_hashes, f, indent=2, ensure_ascii=False)
                
            self.run_post_deploy_commands()
            print("\n[OK] Deployment completed successfully!")
            
        return success


def main():
    parser = argparse.ArgumentParser(
        description="Vanguard Technologies Production Deployer",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--mode', choices=['test', 'deploy', 'deploy-all'], default='deploy',
                        help='Deploy mode (test: test credentials, deploy: delta deploy, deploy-all: upload all files)')
    args = parser.parse_args()

    try:
        manager = DeploymentManager()
        if args.mode == 'test':
            manager.test_connection()
        elif args.mode == 'deploy':
            manager.deploy(all_files=False)
        elif args.mode == 'deploy-all':
            manager.deploy(all_files=True)
    except KeyboardInterrupt:
        print("\n[Info] Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
