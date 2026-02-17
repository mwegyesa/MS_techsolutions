# Odoo Custom Signin Application

A custom Odoo 12 application with a modern signin/login interface and dashboard.

## Features

- Custom login page with modern UI
- Custom homepage
- User dashboard with role-based access
- Product management
- User management
- Custom logout functionality

## Prerequisites

- Docker
- Docker Compose
- Git

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd odoo
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
- Homepage: http://localhost:8069/custom-home
- Login: http://localhost:8069/my-signin
- Dashboard: http://localhost:8069/my-dashboard

4. Default credentials:
- Username: admin
- Password: admin

## Project Structure

```
.
├── addons/
│   └── signin/              # Custom signin module
│       ├── controllers/     # Route controllers
│       ├── views/          # XML templates
│       └── static/         # Static assets
├── docker-compose.yml      # Docker configuration
├── Dockerfile             # Custom Docker image (if needed)
└── odoo.conf             # Odoo configuration
```

## Deployment Options

### ⚠️ Important: Vercel is NOT suitable for Odoo

Odoo cannot be deployed on Vercel because:
- Vercel is for static sites and serverless functions
- Odoo requires a persistent PostgreSQL database
- Odoo needs long-running Python processes
- Odoo requires persistent file storage

### Recommended Deployment Platforms:

1. **DigitalOcean App Platform**
   - Supports Docker containers
   - Managed PostgreSQL database
   - Easy scaling
   - Cost: ~$12/month

2. **Heroku**
   - Docker container support
   - Heroku Postgres add-on
   - Easy deployment with Git
   - Cost: ~$7-25/month

3. **AWS (Elastic Beanstalk or ECS)**
   - Full control
   - Scalable
   - RDS for PostgreSQL
   - Cost: Variable

4. **Railway.app**
   - Docker support
   - Built-in PostgreSQL
   - Simple deployment
   - Cost: ~$5-20/month

5. **Render.com**
   - Docker support
   - Managed PostgreSQL
   - Free tier available
   - Cost: Free - $25/month

### Deployment Steps (Generic):

1. **Prepare your repository:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Set up environment variables:**
   - `DB_HOST`: PostgreSQL host
   - `DB_PORT`: PostgreSQL port (usually 5432)
   - `DB_USER`: Database user
   - `DB_PASSWORD`: Database password
   - `DB_NAME`: Database name

3. **Deploy using Docker:**
   Most platforms support deploying from a `docker-compose.yml` file or Dockerfile.

## Module Installation

After deployment, install the custom module:

1. Go to Apps menu
2. Update Apps List
3. Search for "Signin Page"
4. Click Install

## Upgrading the Module

After making changes to the code:

```bash
docker exec odoo odoo -u signin -d <database-name> --stop-after-init
docker-compose restart odoo
```

Or through the UI:
1. Go to Apps menu
2. Search for "Signin Page"
3. Click Upgrade

## Troubleshooting

### Routes not working
- Ensure the module is installed and upgraded
- Check container logs: `docker logs odoo`
- Restart containers: `docker-compose restart`

### Database connection issues
- Verify PostgreSQL is running: `docker ps`
- Check database credentials in `odoo.conf`
- Ensure database exists

### Session/Login issues
- Clear browser cookies
- Check if session is being maintained
- Verify authentication in controller

## License

This project is for educational/commercial use.

## Support

For issues and questions, please create an issue in the GitHub repository.
