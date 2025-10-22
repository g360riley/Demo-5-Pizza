# Pizza Management System - Deployment Guide

## Production Deployment Checklist

### 1. Environment Setup

#### Update .env file for production:
```bash
DB_HOST=your-production-mysql-host
DB_USER=your-production-user
DB_PASSWORD=your-strong-password
DB_NAME=your-production-database
SECRET_KEY=generate-a-strong-secret-key-here
```

#### Generate a strong SECRET_KEY:
```python
import secrets
print(secrets.token_hex(32))
```

### 2. Database Setup

#### Create production database:
```sql
CREATE DATABASE your_production_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON your_production_database.* TO 'your-production-user'@'%';
FLUSH PRIVILEGES;
```

#### Initialize database tables:
```bash
python app/init_db.py
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Production Server Setup

#### Using Gunicorn (Recommended):

```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app:app

# Run in background with logging
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 --access-logfile access.log --error-logfile error.log --daemon app:app
```

#### Systemd Service (Linux):

Create `/etc/systemd/system/pizza-management.service`:

```ini
[Unit]
Description=Pizza Management System
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Demo-5-Pizza
Environment="PATH=/path/to/Demo-5-Pizza/venv/bin"
ExecStart=/path/to/Demo-5-Pizza/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pizza-management
sudo systemctl start pizza-management
sudo systemctl status pizza-management
```

### 5. Nginx Reverse Proxy Setup

Create `/etc/nginx/sites-available/pizza-management`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/Demo-5-Pizza/app/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/pizza-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL/HTTPS Setup (Using Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 7. Security Considerations

#### Database Security:
- Use strong passwords
- Restrict database access to application server IP only
- Enable SSL for database connections
- Regular backups

#### Application Security:
- Change default employee passwords
- Use strong SECRET_KEY
- Enable HTTPS only
- Implement rate limiting (consider Flask-Limiter)
- Regular security updates

#### Firewall Setup:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 8. Monitoring and Logging

#### Application Logs:
```bash
# View Gunicorn logs
tail -f access.log error.log

# View systemd logs
sudo journalctl -u pizza-management -f
```

#### Database Monitoring:
- Monitor connection pool usage
- Track slow queries
- Set up automated backups

### 9. Backup Strategy

#### Database Backups:
```bash
# Daily backup script
mysqldump -u user -p database_name > backup_$(date +%Y%m%d).sql

# Automated backup with cron
0 2 * * * /path/to/backup_script.sh
```

#### Application Backups:
- Version control with Git
- Backup .env file separately (encrypted)
- Regular code snapshots

### 10. Performance Optimization

#### Gunicorn Workers:
```bash
# Calculate optimal workers: (2 x CPU cores) + 1
gunicorn -w 9 -b 0.0.0.0:8000 app:app  # For 4 CPU cores
```

#### Database Optimization:
- Enable query caching
- Add indexes on frequently queried columns (already included)
- Use connection pooling
- Consider read replicas for high traffic

#### Caching:
Consider adding Flask-Caching for:
- Dashboard statistics
- Pizza menu data
- Customer lookups

### 11. Cloud Deployment Options

#### AWS EC2:
1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies
3. Configure RDS for MySQL
4. Set up Elastic Load Balancer
5. Use Route 53 for DNS

#### Heroku:
1. Create Procfile: `web: gunicorn app:app`
2. Use ClearDB MySQL add-on
3. Set environment variables
4. Deploy: `git push heroku main`

#### DigitalOcean:
1. Create Droplet (Ubuntu 22.04)
2. Use Managed MySQL Database
3. Configure Nginx
4. Set up Let's Encrypt SSL

### 12. Testing Production Deployment

```bash
# Test database connection
python -c "from app.db_connect import get_db; print('DB OK' if get_db() else 'DB Failed')"

# Test application
curl http://localhost:8000

# Load testing
ab -n 1000 -c 10 http://localhost:8000/
```

### 13. Maintenance

#### Regular Updates:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart application
sudo systemctl restart pizza-management
```

#### Database Maintenance:
```sql
-- Optimize tables
OPTIMIZE TABLE customers, pizzas, orders, order_details, employees;

-- Check table integrity
CHECK TABLE customers, pizzas, orders, order_details, employees;
```

### 14. Troubleshooting

#### Common Issues:

**Database Connection Errors:**
- Verify .env file configuration
- Check database server is running
- Verify firewall rules
- Check user permissions

**502 Bad Gateway:**
- Ensure Gunicorn is running
- Check Nginx configuration
- Verify port bindings

**Permission Errors:**
- Check file ownership
- Verify service user permissions
- Review log file permissions

### 15. Scaling Strategy

#### Horizontal Scaling:
- Multiple Gunicorn instances
- Load balancer (Nginx, HAProxy)
- Shared MySQL database or read replicas
- Session management (Redis/Memcached)

#### Vertical Scaling:
- Increase server resources
- Optimize database queries
- Add caching layers
- CDN for static assets

---

## Quick Production Start

```bash
# 1. Set environment variables
export DB_HOST=your-host
export DB_USER=your-user
export DB_PASSWORD=your-password
export DB_NAME=your-database
export SECRET_KEY=your-secret-key

# 2. Initialize database
python app/init_db.py

# 3. Start production server
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Support

For production issues:
1. Check application logs
2. Review database logs
3. Verify environment variables
4. Test database connectivity
5. Review Nginx/proxy logs
