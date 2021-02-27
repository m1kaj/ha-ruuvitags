import logging
from aiohttp import web
from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive

allData = {}

async def get_data_from_all_tags(request):
    return web.json_response(allData)

async def get_data_from_tag(request):
    mac = request.match_info.get('mac').upper()
    if mac not in allData:
        return web.json_response(status=404)
    return web.json_response(allData[mac])

def setup_routes(app):
    app.router.add_get('/ruuvitags', get_data_from_all_tags)
    app.router.add_get('/ruuvitag/{mac}', get_data_from_tag)

if __name__ == '__main__':

    tags = {
        "E6:E7:17:85:8D:0F": "ruuvitag 1",
        "D9:64:A3:18:73:97": "ruuvitag 2"
    }

    class BlesonLogFilter(logging.Filter):
        def __init__(self, filter_text):
            self.filter_text = filter_text
        
        def filter(self, record):
            return self.filter_text not in record.getMessage()
    
    def handle_new_data(data):
        global allData
        data[1]['name'] = tags[data[0]]
        allData[data[0]] = data[1]

    # drop all TODO type error messages from bleson logger
    bleson_filt = BlesonLogFilter("TODO:")
    for name, logger in logging.root.manager.loggerDict.items():
        if "bleson" in name:
            logger.addFilter(bleson_filt)

    # start receiving data from ruuvitags
    ruuvi_rx = RuuviTagReactive(list(tags.keys()))
    data_stream = ruuvi_rx.get_subject()
    data_stream.subscribe(handle_new_data)

    # Setup and start web application
    app = web.Application()
    setup_routes(app)
    web.run_app(app, host='0.0.0.0', port=5150)