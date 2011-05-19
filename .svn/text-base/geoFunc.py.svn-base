import math

MERCATOR_RANGE = 256
 
def bound(value, opt_min=None, opt_max=None):
    if opt_min != None:
          value = max(value, opt_min)
    if opt_max != None:
          value = min(value, opt_max)
    return value

def degreesToRadians(deg):
    return deg * (math.pi / 180)

class MercatorProjection:
    def __init__(self):
        self.pixelOrigin_ = {'x':MERCATOR_RANGE / 2.0, 'y':MERCATOR_RANGE / 2.0}
        self.pixelsPerLonDegree_ = MERCATOR_RANGE / 360.0
        self.pixelsPerLonRadian_ = MERCATOR_RANGE / (2.0 * math.pi)

    def LL_Pt(self, latLng, zoom=0, output=False, opt_point=False, tileBool=False):
        point = opt_point and opt_point or {'x':0, 'y':0}
        point['x'] = self.pixelOrigin_['x'] + latLng['lng'] * self.pixelsPerLonDegree_;
        siny = bound(math.sin(degreesToRadians(latLng['lat'])), -0.9999, 0.9999)
        point['y'] = self.pixelOrigin_['y'] - 0.5 * math.log((1 + siny) / (1 - siny)) * self.pixelsPerLonRadian_
        pixel = {'x':point['x'] * math.pow(2, zoom), 'y':point['y'] * math.pow(2, zoom)}
        tile = {'x':math.floor(pixel['x'] / MERCATOR_RANGE), 'y':math.floor(pixel['y'] / MERCATOR_RANGE)}
        if tileBool:
            return pixel, tile
        else:
            return pixel

    def Tile_LL(self, tile, zoom=0, output=False):
        latLng = {'lat':[], 'lng':[]}
        pixel = {'x':float(tile['x'] * MERCATOR_RANGE), 'y':float(tile['y'] * MERCATOR_RANGE)}
        point = {'x':pixel['x'] / math.pow(2, zoom), 'y':pixel['y'] / math.pow(2, zoom)}
        z = math.exp(2 * (self.pixelOrigin_['y'] - point['y']) / self.pixelsPerLonRadian_)
        latLng['lat'].append((180. / math.pi) * math.asin(bound((z - 1) / (z + 1), -1, 1)))            
        latLng['lng'].append((point['x'] - self.pixelOrigin_['x']) / self.pixelsPerLonDegree_)

        pixel = {'x':float((1 + tile['x']) * MERCATOR_RANGE), 'y':float((1 + tile['y']) * MERCATOR_RANGE)}
        point = {'x':pixel['x'] / math.pow(2, zoom), 'y':pixel['y'] / math.pow(2, zoom)}
        z = math.exp(2 * (self.pixelOrigin_['y'] - point['y']) / self.pixelsPerLonRadian_)
        latLng['lat'].append((180. / math.pi) * math.asin(bound((z - 1) / (z + 1), -1, 1)))            
        latLng['lng'].append((point['x'] - self.pixelOrigin_['x']) / self.pixelsPerLonDegree_)

        return {'tile':[[latLng['lng'][0], latLng['lat'][0]], [latLng['lng'][1], latLng['lat'][0]],
                        [latLng['lng'][1], latLng['lat'][1]], [latLng['lng'][0], latLng['lat'][1]],
                        [latLng['lng'][0], latLng['lat'][0]]],
                'x': pixel['x'] - MERCATOR_RANGE, 'y': pixel['y'] - MERCATOR_RANGE}

##mp = MercatorProjection()
##print mp.LL_Pt(latLng={'lat':41.850033, 'lng':-87.6500523}, zoom=4)
##print mp.Tile_LL(tile={'y':5, 'x':4}, zoom=4)
