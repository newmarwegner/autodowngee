# Download NDVI image collection from gee (Landsat 7)

These script was built to download images from gee collection images considering a specific area delimited by shapefile.

## Steps to run
1. Clone repository
2. Create and activate a venv 
3. Insert shapefile of your area in "dados" folder
4. Config parameters in main.py code
    - start_date='1999-01-01' # insert initial date
    - end_date='2001-04-25'   # insert end date
    - filter_field = 'id'     # insert name of atribute field to filter shapefile

### Codes
```python
git clone https://github.com/newmarwegner/autodowngee.git
python -m venv .venv
source autogee_ndvi/bin/activate
```
