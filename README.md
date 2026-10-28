# PDF Studio

Browser PDF tool: merge, reorder, crop, edit, OCR, compress, convert.

## Deploy on Vercel
1. Push this whole folder (index.html, api/, requirements.txt, vercel.json) to a GitHub repo.
2. Vercel > Add New > Project > import the repo. Framework Preset: Other. Deploy.

## Notes
- PDF to Word and PDF to Excel run in `api/convert.py` (pdf2docx + PyMuPDF). Vercel limits request size to 4.5 MB, so convert big PDFs in parts.
- Everything else (crop, edit, OCR, Word to PDF, images) runs in the browser.
