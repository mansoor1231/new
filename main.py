from fastapi import  FastAPI, status
import psycopg2
import re
print("Connecting")

# conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
#                             password="brocafe", port=5432)
# conn = psycopg2.connect(host=host_name, dbname=database_name, user=user_name,
#                             password=user_pass, port=port_name)
conn = psycopg2.connect(host="fastapi-server.postgres.database.azure.com", dbname="postgres", user="plantfastapi",
                            password="IOTmonitor1!", port=5432)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS soil_monitor (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    time TIME NOT NULL DEFAULT CURRENT_TIME,
    DeviceName VARCHAR(255),
    LightIntensity FLOAT,
    SoilMoisture FLOAT,
    Humidity FLOAT,
    Temperature FLOAT);""")
conn.commit()
print("Connected")
app = FastAPI()

@app.get("/", status_code = status.HTTP_200_OK)
async def root():
    return {"Plant": "hello world"}
@app.post("/", status_code = status.HTTP_200_OK)
async def post():
    return {"message": "hello post"}
@app.get("/get", status_code = status.HTTP_200_OK)
async def get_info():
    # cur = conn.cursor()
    cur.execute("""SELECT *
        FROM soil_monitor
        ORDER BY id DESC
        LIMIT 1;""")
    conn.commit()
    result = cur.fetchone()
    print(result)

    int_value = int(result[0])
    date = result[1]
    time = result[2]
    device_name = result[3]
    light = int(result[4])
    soil = int(result[5])
    humid = int(result[6])
    temp = int(result[7])
    # int_value = 25
    # date = "2024/03/19"
    # time = "13:10:44"
    # device_name = "Pi"
    # light = 3.54
    # soil = 5.48
    # humid = 60.4
    # temp = 32.45
    # Print the extracted values
    print("Integer:", int_value)
    print("Time:", time)
    print("Date:", date)
    print("Device Name:", device_name)
    print("Lght Intensity:%fcd" % light)
    print("Soil Moisture:%fm~/m3" % soil)
    print("Humidity:%f%%" % humid)
    print("Temperature:%f°C" % temp)
    return {"Date:":date,"Time:":time,"Device Name:":device_name,
            "Light Intensity:":light,"Soil Moisture:":soil,"Humidity:":humid,"Temperature:":temp
            }

@app.get("/post/{dname}", status_code = status.HTTP_200_OK)
async def post_data(dname: str):
    #                name,  light, soil,humid, temp
    # data_string = "device_25.23_45.68_125.25_23.751"

    pattern = r'([^_]+)_([-+]?[0-9]*\.?[0-9]+)_([-+]?[0-9]*\.?[0-9]+)_([-+]?[0-9]*\.?[0-9]+)_([-+]?[0-9]*\.?[0-9]+)'
    match = re.match(pattern, dname)
    if match:
        device = match.group(1)
        light = float(match.group(2))
        soil = float(match.group(3))
        humid = float(match.group(4))
        temp = float(match.group(5))
        # Print the extracted components
        print("Device:", device)
        print("Float 1:", light)
        print("Float 2:", soil)
        print("Float 3:", humid)
        print("Float 4:", temp)
    else:
        print("No match found.")
        device = ""
        light = 0
        soil = 0
        humid = 0
        temp = 0
    # conn = psycopg2.connect(host="localhost", dbname="fastapi", user="postgres",
    #                         password="brocafe", port=5432)
    # cur = conn.cursor()
    cur.execute("""INSERT INTO soil_monitor (DeviceName, LightIntensity, SoilMoisture, Humidity, Temperature) VALUES
    ('"""+device+"""', %f, %f, %f,%f);
    """ % ( light, soil , humid, temp))
    conn.commit()
    # cur.close()
    # conn.close()
    return {"#Data Posted":dname}