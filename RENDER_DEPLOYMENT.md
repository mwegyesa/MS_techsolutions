# Deploying Odoo to Render.com (Free Tier)

This guide will help you deploy your Odoo application to Render.com's free tier.

## Prerequisites

- GitHub account
- Render.com account (sign up at https://render.com)
- Your code pushed to GitHub repository

## Important Limitations of Render Free Tier

⚠️ **Free tier limitations:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month of runtime
- Limited resources (512MB RAM)
- PostgreSQL database has 90-day expiration on free tier

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

```bash
# If not already done
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/MS_techsolutions.git
git push -u origin main
```

### 2. Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `odoo-db`
   - **Database**: `odoo`
   - **User**: `odoo`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click "Create Database"
5. **Save the connection details** (Internal Database URL)

### 3. Create Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository `MS_techsolutions`
3. Configure:
   - **Name**: `odoo-web`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Plan**: Free

4. **Environment Variables** (Add these):
   ```
   HOST=<your-postgres-internal-host>
   PORT=5432
   USER=odoo
   PASSWORD=<your-postgres-password>
   DB_NAME=odoo
   ```
   
   Get these values from your PostgreSQL database's "Internal Database URL":
   `postgresql://USER:PASSWORD@HOST:PORT/DB_NAME`

5. **Advanced Settings**:
   - **Docker Command**: Leave empty (uses default from Dockerfile)
   - **Health Check Path**: `/web/health` (optional)

6. Click "Create Web Service"

### 4. Wait for Deployment

- Initial deployment takes 5-10 minutes
- Watch the logs for any errors
- Once deployed, you'll get a URL like: `https://odoo-web.onrender.com`

### 5. Access Your Application

1. Visit: `https://your-app-name.onrender.com/custom-home`
2. Login at: `https://your-app-name.onrender.com/my-signin`
3. Default credentials:
   - Username: `admin`
   - Password: `admin`

### 6. Install the Custom Module

1. Go to: `https://your-app-name.onrender.com/web`
2. Login with admin credentials
3. Go to Apps menu
4. Click "Update Apps List"
5. Search for "Signin Page"
6. Click "Install"

## Troubleshooting

### Service Won't Start

**Check logs in Render dashboard:**
- Database connection issues: Verify environment variables
- Port conflicts: Ensure using port 8069
- Memory issues: Free tier has limited RAM

### Database Connection Failed

1. Verify PostgreSQL service is running
2. Check environment variables match database credentials
3. Ensure using **Internal Database URL** (not External)

### Module Not Found

1. Ensure `addons` folder is in repository
2. Check `odoo.conf` has correct `addons_path`
3. Restart the service

### Slow Performance

- Free tier spins down after inactivity
- First request after spin-down is slow
- Consider upgrading to paid tier for production

## Upgrading to Paid Tier

For production use, consider:
- **Starter Plan** ($7/month): No spin-down, better performance
- **PostgreSQL Standard** ($7/month): No 90-day expiration

## Alternative: Using Docker Compose (Not Recommended for Free Tier)

Render's free tier doesn't support docker-compose directly. You need to:
1. Create separate services for web and database
2. Connect them via environment variables
3. Use the steps above

## Monitoring

- Check logs: Render Dashboard → Your Service → Logs
- Monitor uptime: Render Dashboard → Your Service → Metrics
- Set up alerts: Render Dashboard → Your Service → Settings → Notifications

## Backup Your Database

⚠️ **Important**: Free PostgreSQL expires after 90 days!

To backup:
1. Go to your PostgreSQL service
2. Click "Connect" → Get connection string
3. Use `pg_dump` to backup:
   ```bash
   pg_dump <connection-string> > backup.sql
   ```

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Odoo Docs: https://www.odoo.com/documentation/12.0

## Next Steps

After successful deployment:
1. Change admin password
2. Configure email settings
3. Set up custom domain (optional)
4. Enable HTTPS (automatic on Render)
5. Monitor application performance
