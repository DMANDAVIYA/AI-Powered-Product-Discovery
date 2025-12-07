# Database Migration Guide

## 🎯 Problem: Don't Want to Re-scrape on Production

**Solution:** Export local data → Import on production (NO API calls!)

---

## 📤 Step 1: Export Local Database

**On your local machine (Windows):**

```bash
# Run export script
.venv\Scripts\python -m backend.export_db
```

**This creates:**
- ✅ `products_backup.json` - All 25 products (PostgreSQL data)
- ✅ `chroma_db_backup/` - Vector embeddings (ChromaDB)

---

## 📦 Step 2: Add Backup Files to Git

```bash
# Add backup files
git add products_backup.json

# Commit
git commit -m "Add database backup for migration"

# Push to GitHub
git push
```

**Note:** `chroma_db_backup/` is gitignored (too large). We'll regenerate vectors on import.

---

## 📥 Step 3: Import on Production

**After deploying to Render:**

### Option A: Using Render Shell

1. Go to Render dashboard
2. Click on your web service
3. Click "Shell" tab
4. Run:
```bash
python -m backend.import_db
```

### Option B: Add Import Endpoint

Add this to `backend/main.py`:

```python
@app.post("/import-backup")
def import_backup():
    """Import products from backup JSON"""
    try:
        from .import_db import import_database
        import_database()
        return {"message": "Import completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Then call:
```bash
curl -X POST https://neusearch-backend.onrender.com/import-backup
```

---

## 💰 Cost Comparison

### Re-scraping (Original Method):
- **Firecrawl API:** 25 URLs × 1 credit = 25 credits
- **OpenAI Embeddings:** 25 products × ~$0.0001 = ~$0.0025
- **Total:** ~25 Firecrawl credits + $0.0025

### Migration (This Method):
- **Firecrawl API:** 0 credits ✅
- **OpenAI Embeddings:** 25 products × ~$0.0001 = ~$0.0025
- **Total:** $0.0025 only!

**Savings:** 25 Firecrawl credits!

---

## 🔄 Complete Migration Workflow

```
LOCAL MACHINE:
1. python -m backend.export_db
   → Creates products_backup.json
   
2. git add products_backup.json
3. git commit -m "Add backup"
4. git push

PRODUCTION (Render):
5. Deploy completes
6. Call /import-backup endpoint
   OR
   Run: python -m backend.import_db
   
7. Wait 30 seconds
8. Done! ✅
```

---

## ⚠️ Important Notes

### ChromaDB Vectors:
- **Not included in backup** (too large for Git)
- **Regenerated on import** using OpenAI API
- **Cost:** ~$0.0025 (very cheap!)

### If You Run Out of OpenAI Credits:
You can still import products to PostgreSQL, but:
- ❌ Vector search won't work
- ❌ Chat will fail
- ✅ Product listing works
- ✅ Product details work

**Solution:** Add $5 to OpenAI account (lasts months)

---

## 🎯 Recommended Approach

**For Assignment Submission:**

1. **Export locally** (run `export_db.py`)
2. **Push backup to GitHub**
3. **Deploy to Render**
4. **Import on production** (run `import_db.py`)
5. **Done!** No re-scraping needed

**Benefits:**
- ✅ Saves Firecrawl credits
- ✅ Faster deployment
- ✅ Same data as local
- ✅ Professional approach

---

## 📝 Files Created

- ✅ `backend/export_db.py` - Export script
- ✅ `backend/import_db.py` - Import script
- ✅ `MIGRATION.md` - This guide

**Ready to export your database?**

```bash
.venv\Scripts\python -m backend.export_db
```
