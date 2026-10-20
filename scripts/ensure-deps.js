import fs from 'fs';
import { execSync } from 'child_process';

const nodeModulesExists = fs.existsSync('node_modules');
const viteExists = fs.existsSync('node_modules/vite');

if (!nodeModulesExists || !viteExists) {
  console.log('📦 Chưa tìm thấy thư viện (node_modules). Đang tự động chạy npm install...');
  try {
    execSync('npm install', { stdio: 'inherit', shell: true });
    console.log('✅ Cài đặt thư viện thành công! Bắt đầu khởi động ứng dụng...\n');
  } catch (error) {
    console.error('❌ Lỗi trong quá trình tự động chạy npm install:', error);
    process.exit(1);
  }
}
