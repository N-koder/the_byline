# Django Deployment Checklist - Fix for 500 Server Error

## Issues Fixed:

### 1. ✅ Corrupted requirements.txt
- **Problem**: File had encoding issues with null bytes
- **Solution**: Recreated clean requirements.txt file

### 2. ✅ Database Configuration
- **Problem**: Using localhost settings for production
- **Solution**: Added DATABASE_URL support with fallback

### 3. ✅ Search Query Logic Error
- **Problem**: Using Python `or` instead of Django `|` in Q objects
- **Solution**: Changed `or` to `|` in search filter

### 4. ✅ Missing Production Settings
- **Problem**: No logging, security settings, or CSRF configuration
- **Solution**: Added proper production configuration

### 5. ✅ Static Files Configuration
- **Problem**: Missing STATIC_ROOT and proper storage backend
- **Solution**: Configured WhiteNoise with proper settings

## Deployment Steps:

### For Your Hosting Platform (Render/Heroku/etc.):

1. **Set Environment Variables** (use values from .env.production):
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=thebyline.in,www.thebyline.in,your-hosting-domain.com
   DATABASE_URL=postgresql://username:password@host:port/database_name
   CLOUDFLARE_ACCESS_KEY_ID=your-key
   CLOUDFLARE_SECRET_ACCESS_KEY=your-secret
   CLOUDFLARE_STORAGE_BUCKET_NAME=thebyline-media
   CLOUDFLARE_R2_ENDPOINT=your-endpoint
   CLOUDFLARE_R2_CUSTOM_DOMAIN=your-domain
   RAPIDAPI_CRICKBUZZ_KEY=your-api-key
   ```

2. **Deploy Updated Code**:
   - Push all changes to your repository
   - Trigger deployment on your hosting platform

3. **Run Migrations** (if needed):
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Create Superuser** (if needed):
   ```bash
   python manage.py createsuperuser
   ```

## Critical Points:

- ✅ **DEBUG=False** in production
- ✅ **DATABASE_URL** must be set by hosting service
- ✅ **ALLOWED_HOSTS** must include your domain
- ✅ **SECRET_KEY** should be different from development
- ✅ **Static files** will be served by WhiteNoise
- ✅ **Media files** will be served by Cloudflare R2

## Testing:

After deployment, test:
- [ ] Homepage loads without 500 error
- [ ] Static files (CSS, images) load correctly
- [ ] Search functionality works
- [ ] Article pages load
- [ ] Admin panel accessible

## If Still Getting 500 Errors:

1. Check hosting platform logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure database is accessible
4. Check that migrations have been run
5. Verify static files have been collected

The main issues causing your 500 error were:
1. Corrupted requirements.txt
2. Wrong search query syntax (Python `or` vs Django `|`)
3. Missing production database configuration
4. Missing logging to see actual errors