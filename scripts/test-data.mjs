import fs from 'fs';
import path from 'path';

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✓ PASS: ${message}`);
    passed++;
  } else {
    console.error(`  ✗ FAIL: ${message}`);
    failed++;
  }
}

console.log('=== KIỂM THỬ TỰ ĐỘNG DỮ LIỆU & TÍNH TOÀN VẸN (STAGE 8) ===\n');

// 1. Kiểm tra tồn tại và cú pháp file JSON
console.log('1. Kiểm tra file dữ liệu:');
const bookPath = path.resolve('src/data/book.json');
const entriesPath = path.resolve('src/data/entries.json');

assert(fs.existsSync(bookPath), 'src/data/book.json tồn tại');
assert(fs.existsSync(entriesPath), 'src/data/entries.json tồn tại');

const bookData = JSON.parse(fs.readFileSync(bookPath, 'utf-8'));
const entriesData = JSON.parse(fs.readFileSync(entriesPath, 'utf-8'));

assert(bookData && Array.isArray(bookData.lessons), 'book.json có cấu trúc lessons hợp lệ');
assert(Object.keys(entriesData).length > 0, `entries.json chứa ${Object.keys(entriesData).length} từ vựng`);

// 2. Kiểm tra tham chiếu ID
console.log('\n2. Kiểm tra tính toàn vẹn tham chiếu ID:');
const allEntryIds = new Set(Object.keys(entriesData));
let referencedIds = new Set();
let invalidRefs = [];

// Ignored proper names as per user requirement (strictly meaningful vocabulary only, no character names)
const EXCLUDED_PROPER_NAMES = new Set(['nam', 'ha', 'di_kha', 'le_quy_don']);

for (const lesson of bookData.lessons) {
  // Check nhanBiet tokens
  for (const token of lesson.nhanBiet.tokens) {
    if (token.entryId && !EXCLUDED_PROPER_NAMES.has(token.entryId)) {
      referencedIds.add(token.entryId);
      if (!allEntryIds.has(token.entryId)) {
        invalidRefs.push(`Lesson ${lesson.id} nhanBiet: ${token.entryId}`);
      }
    }
  }

  // Check tapDoc tokens
  for (const token of lesson.tapDoc.tokens) {
    if (token.entryId && !EXCLUDED_PROPER_NAMES.has(token.entryId)) {
      referencedIds.add(token.entryId);
      if (!allEntryIds.has(token.entryId)) {
        invalidRefs.push(`Lesson ${lesson.id} tapDoc: ${token.entryId}`);
      }
    }
  }

  // Check docTuNgu
  for (const w of lesson.docTuNgu) {
    if (w.entryId && !EXCLUDED_PROPER_NAMES.has(w.entryId)) {
      referencedIds.add(w.entryId);
      if (!allEntryIds.has(w.entryId)) {
        invalidRefs.push(`Lesson ${lesson.id} docTuNgu: ${w.entryId}`);
      }
    }
  }
}

assert(invalidRefs.length === 0, `Tất cả ID được tham chiếu đều tồn tại trong từ điển (lỗi: ${invalidRefs.join(', ') || 'Không'})`);
assert(referencedIds.size > 0, `Đã tham chiếu thành công ${referencedIds.size} mục từ khác nhau trong sách`);

// 3. Kiểm tra số nghĩa tiếng Anh (tối đa 2 nghĩa theo quy định)
console.log('\n3. Kiểm tra giới hạn số nghĩa tiếng Anh (tối đa 2 nghĩa/từ):');
let exceededMeanings = [];
for (const [id, entry] of Object.entries(entriesData)) {
  if (entry.meaningsEn.length > 2) {
    exceededMeanings.push(`${id} có ${entry.meaningsEn.length} nghĩa`);
  }
}
assert(exceededMeanings.length === 0, `Mọi từ vựng đều có tối đa 2 nghĩa tiếng Anh theo ngữ cảnh (${exceededMeanings.join(', ') || 'Đạt'})`);

// 4. Kiểm tra file âm thanh cục bộ
console.log('\n4. Kiểm tra file âm thanh cục bộ:');
let missingAudioVi = 0;
let missingAudioEn = 0;

for (const [id, entry] of Object.entries(entriesData)) {
  const viFile = path.resolve('public' + entry.audioVi);
  const enFile = path.resolve('public' + entry.audioEn);

  if (!fs.existsSync(viFile)) missingAudioVi++;
  if (!fs.existsSync(enFile)) missingAudioEn++;
}

assert(missingAudioVi === 0, `Tất cả ${Object.keys(entriesData).length} file âm thanh Tiếng Việt đều tồn tại trên đĩa`);
assert(missingAudioEn === 0, `Tất cả ${Object.keys(entriesData).length} file âm thanh Tiếng Anh đều tồn tại trên đĩa`);

// 5. Kiểm tra khả năng tái dựng câu từ token
console.log('\n5. Kiểm tra tái dựng câu từ tokens:');
let reconstructedMismatch = 0;
for (const lesson of bookData.lessons) {
  const reconstructedNhanBiet = lesson.nhanBiet.tokens.map(t => t.text).join('');
  if (reconstructedNhanBiet !== lesson.nhanBiet.sentence) {
    reconstructedMismatch++;
    console.error(`Mismatch nhanBiet L${lesson.lessonNumber}: "${reconstructedNhanBiet}" vs "${lesson.nhanBiet.sentence}"`);
  }

  const reconstructedTapDoc = lesson.tapDoc.tokens.map(t => t.text).join('');
  if (reconstructedTapDoc !== lesson.tapDoc.sentence) {
    reconstructedMismatch++;
    console.error(`Mismatch tapDoc L${lesson.lessonNumber}: "${reconstructedTapDoc}" vs "${lesson.tapDoc.sentence}"`);
  }
}
assert(reconstructedMismatch === 0, '100% tokens tái dựng khớp hoàn hảo câu văn chuẩn hóa (không mất khoảng trắng, không mất dấu câu)');

// 6. Kiểm tra các file Markdown chuẩn hóa
console.log('\n6. Kiểm tra Markdown files:');
const markdownDir = path.resolve('data/markdown');
const mdFiles = fs.readdirSync(markdownDir).filter(f => f.endsWith('.md'));
assert(mdFiles.length >= 21, `Đã tạo đầy đủ ${mdFiles.length} file Markdown chuẩn hóa cho các bài học`);

console.log(`\n========================================`);
console.log(`KẾT QUẢ: ${passed} PASS, ${failed} FAIL`);
console.log(`========================================\n`);

if (failed > 0) {
  process.exit(1);
}
