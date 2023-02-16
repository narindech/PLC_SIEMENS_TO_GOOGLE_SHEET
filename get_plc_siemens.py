import snap7
from snap7 import util
import pandas as pd

# resource for pandas ====> https://towardsdatascience.com/using-python-to-push-your-pandas-dataframe-to-google-sheets-de69422508f
# resource ----> https://automation360blog.wordpress.com/2022/09/21/python_snap7/
# documentation ----> https://python-snap7.readthedocs.io/en/latest/API/client.html

PUMP_DB_NUMBER = 1
HMI_DB_NUMBER = 2
PLC_IP_ADDRESS = 'PUT_YOUR_PLC_IP_ADDRESS_HERE'

def get_plc_db():
	try:
		client = snap7.client.Client()
		client.connect(PLC_IP_ADDRESS, 0, 1)
		client.get_connected()		
	except Exception as e:
		print(f"Error occurred : {e}")
		return None

	"""
		PUMPDB (DB1)
	"""

	start_pump = client.db_read(PUMP_DB_NUMBER, 0, 1)
	start_pump_val = util.get_bool(start_pump, 0, 0)

	stop_pump = client.db_read(PUMP_DB_NUMBER, 0, 1)
	stop_pump_val = util.get_bool(stop_pump, 0, 1)

	mode_control = client.db_read(PUMP_DB_NUMBER, 0, 1)
	mode_control_val = util.get_bool(mode_control, 0, 2)



	"""
		HMI Data (DB2)
	"""
	level_sensor = client.db_read(HMI_DB_NUMBER, 0, 4)
	level_sensor_val = util.get_real(level_sensor, 0)

	flow_rate = client.db_read(HMI_DB_NUMBER, 4, 4)
	flow_rate_val = util.get_real(flow_rate, 0)

	plc_output = client.db_read(HMI_DB_NUMBER, 8, 2)
	plc_output_val = util.get_int(plc_output, 0)

	zero_level = client.db_read(HMI_DB_NUMBER, 10, 1)
	zero_level_val = util.get_bool(zero_level, 0, 0)

	idle_time = client.db_read(HMI_DB_NUMBER, 12, 2)
	idle_time_val = util.get_int(idle_time, 0)

	disturbance = client.db_read(HMI_DB_NUMBER, 14, 4)
	disturbance_val = util.get_real(disturbance, 0)

	level_transmitter = client.db_read(HMI_DB_NUMBER, 18, 2)
	level_transmitter_val = util.get_int(level_transmitter, 0)


	client.disconnect()
	client.destroy()

	# return {
	# 	"start_pump": start_pump_val,
	# 	"stop_pump": stop_pump_val,
	# 	"mode_control": mode_control_val,
	# 	"level_sensor": level_sensor_val,
	# 	"flow_rate": flow_rate_val,
	# 	"plc_output": plc_output_val,
	# 	"zero_level": zero_level_val,
	# 	"idle_time": idle_time_val,
	# 	"disturbance": disturbance_val,
	# 	"level_transmitter": level_transmitter_val
	# }

	return {
		"start_pump": str(start_pump_val),
		"stop_pump": str(stop_pump_val),
		"mode_control": str(mode_control_val),
		"level_sensor": str(level_sensor_val),
		"flow_rate": str(flow_rate_val),
		"plc_output": str(plc_output_val),
		"zero_level": str(zero_level_val),
		"idle_time": str(idle_time_val),
		"disturbance": str(disturbance_val),
		"level_transmitter": str(level_transmitter_val)
	}

def make_data_for_sheet(payload):
	if payload:
		keyList = list(payload.keys())
		valList = list(payload.values())
		return [keyList, valList]

if __name__ == "__main__":
	print(make_data_for_sheet(get_plc_db()))