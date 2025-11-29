# utils.py
import cv2, numpy as np, time
def classify_traffic_light_color(frame, xyxy):
    x1, y1, x2, y2 = map(int, xyxy)
    h, w = y2 - y1, x2 - x1
    if h <= 0 or w <= 0:
        return None

    crop = frame[y1:y2, x1:x2]
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # RED RANGES
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 50])
    upper_red2 = np.array([179, 255, 255])

    # YELLOW
    lower_yellow = np.array([15, 100, 50])
    upper_yellow = np.array([35, 255, 255])

    # GREEN
    lower_green = np.array([36, 50, 50])
    upper_green = np.array([89, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    total = crop.shape[0] * crop.shape[1]

    red_frac = (mask_red > 0).sum() / total
    yellow_frac = (mask_yellow > 0).sum() / total
    green_frac = (mask_green > 0).sum() / total

    colors = {"red": red_frac, "yellow": yellow_frac, "green": green_frac}

    final_color = max(colors, key=colors.get)

    if colors[final_color] < 0.02:
        return None

    return final_color

'''
def classify_traffic_light_color(frame, xyxy):
    x1, y1, x2, y2 = map(int, xyxy)
    h = max(0, y2-y1); w = max(0, x2-x1)
    if h==0 or w==0: return None
    crop = frame[y1:y2, x1:x2]
    if crop.size==0: return None
   hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0,100,50]); upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([160,100,50]); upper_red2 = np.array([179,255,255])
    lower_yellow = np.array([15,100,50]); upper_yellow = np.array([35,255,255])
    lower_green = np.array([36,50,50]); upper_green = np.array([89,255,255])
    mask_r = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2))
    mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_g = cv2.inRange(hsv, lower_green, upper_green)
    total = crop.shape[0]*crop.shape[1]
    red_frac = (mask_r>0).sum()/total; yellow_frac = (mask_y>0).sum()/total; green_frac = (mask_g>0).sum()/total
    vals = {'red': red_frac, 'yellow': yellow_frac, 'green': green_frac}
    col, frac = max(vals.items(), key=lambda x: x[1])
    if frac < 0.02: return None
    return col
'''
def draw_box(frame, xyxy, label=None):
    x1,y1,x2,y2 = map(int, xyxy)
    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
    if label:
        cv2.putText(frame, label, (x1, max(0,y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

class Debouncer:
    def __init__(self, cooldown=2.0):
        self.cooldown = cooldown
        self.last_spoken = {}
    def can_speak(self, key):
        now = time.time()
        if key not in self.last_spoken or now - self.last_spoken[key] > self.cooldown:
            self.last_spoken[key] = now
            return True
        return False
