# Use Python 3.6 Buster for Odoo 12
FROM python:3.6-buster

# Prevent tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /usr/src/odoo

# Update sources to archive.debian.org for old Buster packages
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list \
 && sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    git wget build-essential \
    zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev \
    libssl-dev libreadline-dev libffi-dev curl \
    libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    xfonts-75dpi xfonts-base tzdata \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Install essential Python packages for Odoo 12
RUN pip install \
    psycopg2-binary \
    lxml \
    Babel==2.5.1 \
    Jinja2==2.10.1 \
    Werkzeug==0.14.1 \
    decorator==4.3.0 \
    python-dateutil \
    pytz \
    PyPDF2 \
    requests \
    passlib \
    html2text \
    docutils \
    polib

# Clone Odoo 12 source code
RUN git clone --branch 12.0 --single-branch https://github.com/odoo/odoo.git .

# Expose default Odoo port
EXPOSE 8069

# Set default command
CMD ["python", "odoo-bin", "-c", "odoo.conf"]
