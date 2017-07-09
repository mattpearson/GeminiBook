# vim:sw=4:nu:expandtab:tabstop=4:ai

import websocket
import thread
import time
import json

class level():
  def __init__( self, price, qty ):
    self.price = price
    self.qty = qty
    pass
  def set( price, qty ):
    self.price = price
    self.qty = qty

class GeminiBook:
  def __init__(self):
    self.bids = {}
    self.offers = {}


def printBook( inside = True ):
    if( inside ):
        bestbid = max( gemini.bids )
        bestask = min( gemini.offers )

        str = ''

        bb = gemini.bids[ bestbid ]
        if( bb ):
            str = '%.2f (%.2f) || ' % ( bb.price, bb.qty )

        ba = gemini.offers[ bestask ]
        if( ba ):
            str = str + '%.2f (%.2f)' % ( ba.price, ba.qty )

        print str

    else:
        print 'full depth printing not yet supported.'
        pass


def on_message(ws, message):
    #print('Received: ', message)

    j = json.loads( message )

    events = j['events']
    for r in range( len( events ) ):
        e = events[r]

        try:
            side = e['side']
            price = float(e['price'])
            qty = float(e['remaining'])
            if( side == u'ask'):
                if( qty == 0 ):
                    gemini.offers.pop( price, None )
                else:
                    gemini.offers[ price ] = level( price, qty )
            if( side == u'bid'):
                if( qty == 0 ):
                    gemini.bids.pop( price, None )
                else:
                    gemini.bids[ price ] = level( price, qty )
        except Exception, err:
            print 'Error: %s %s' % ( err, e )
    printBook()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while( True ):
            time.sleep(100)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    gemini = GeminiBook()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/ethusd",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
