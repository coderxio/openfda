# OpenFDA
## JSON File Location
1. https://open.fda.gov/apis/drug/ndc/download/
2. Unzip and rename 'drug-ndc.json'
3. Place JSON file in ./data/ folder

## Run in venv
1. Clone repo
2. Enter repo: `cd OpenFDA`
2. Create virtual environment: `python3 -m venv ./venv`
3. Enter venv: `source venv/bin/activate`
4. Install requirements: `pip3 install -r requirements.txt`
5. Run DB loader: `python app/load_data.py`
6. Run Cherrypy server: `python app/serve_data.py`

## Run in docker
1. First run to load DB: `docker-compose up --build`
2. Once DB created: `docker-compose -f docker-compose.prod.yml up --build`
3. Destroy entire build, including DB: `docker-compose down -v`