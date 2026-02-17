# Render Environment Variables Setup

## Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `odoo-db` (or any name you prefer)
   - **Database**: `odoo`
   - **User**: `odoo`
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 12 or higher
   - **Plan**: **Free**
4. Click "Create Database"
5. Wait for the database to be created (takes 1-2 minutes)

## Step 2: Get Database Connection Details

After the database is created:

1. Click on your PostgreSQL database in the dashboard
2. Scroll down to "Connections"
3. You'll see:
   - **Internal Database URL**: `postgresql://USER:PASSWORD@HOST:PORT/DATABASE`
   - **External Database URL**: (ignore this for now)

Example Internal URL:
```
postgresql://odoo:xyzABC123@dpg-abc123-a.oregon-postgres.render.com:5432/odoo
```

From this URL, extract:
- **HOST**: `dpg-abc123-a.oregon-postgres.render.com`
- **PORT**: `5432`
- **USER**: `odoo`
- **PASSWORD**: `xyzABC123`
- **DATABASE**: `odoo`

## Step 3: Add Environment Variables to Web Service

1. Go back to your Render dashboard
2. Click on your **Web Service** (odoo-web)
3. Go to "Environment" tab
4. Click "Add Environment Variable"

Add these variables one by one:

### Required Variables:

| Key | Value | Example |
|-----|-------|---------|
| `HOST` | Your PostgreSQL internal host | `dpg-abc123-a.oregon-postgres.render.com` |
| `PORT` | PostgreSQL port | `5432` |
| `USER` | PostgreSQL user | `odoo` |
| `PASSWORD` | PostgreSQL password | `xyzABC123` |
| `DB_NAME` | Database name | `odoo` |

### Optional Variables (for better performance):

| Key | Value | Description |
|-----|-------|-------------|
| `ADMIN_PASSWORD` | `your-secure-password` | Odoo master password |
| `WORKERS` | `0` | Number of workers (0 for free tier) |

## Step 4: Save and Deploy

1. After adding all variables, click "Save Changes"
2. Render will automatically redeploy your service
3. Wait for the deployment to complete (5-10 minutes)

## Step 5: Verify Deployment

Once deployed, check the logs:

1. Go to your Web Service
2. Click on "Logs" tab
3. Look for:
   ```
   Waiting for PostgreSQL at <your-host>:5432...
   PostgreSQL check complete. Starting Odoo...
   ```

If you see errors, check:
- Environment variables are correct
- PostgreSQL database is running
- HOST uses the **Internal** URL, not External

## Troubleshooting

### "No open ports detected"

This means Odoo isn't starting. Check:
1. Environment variables are set correctly
2. PostgreSQL database is running
3. Check logs for specific errors

### "Connection refused" or "Database connection failed"

1. Verify you're using the **Internal Database URL**
2. Check that all environment variables match your PostgreSQL credentials
3. Ensure PostgreSQL service is in the same region as your web service

### "Module not found" errors

1. Ensure your code is pushed to GitHub
2. Check that `addons` folder exists in your repository
3. Verify Dockerfile copies the addons correctly

## Quick Copy-Paste Template

After getting your PostgreSQL details, fill this in:

```
HOST=dpg-XXXXX-a.oregon-postgres.render.com
PORT=5432
USER=odoo
PASSWORD=your_password_here
DB_NAME=odoo
```

## Next Steps

After successful deployment:

1. Access your app at: `https://your-service-name.onrender.com`
2. Go to: `https://your-service-name.onrender.com/custom-home`
3. Login at: `https://your-service-name.onrender.com/my-signin`
4. Default credentials: `admin` / `admin`

## Important Notes

⚠️ **Free Tier Limitations:**
- PostgreSQL database expires after 90 days
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Limited to 512MB RAM

For production, consider upgrading to paid tiers.
