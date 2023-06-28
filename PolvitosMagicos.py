// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/


//@version=5
indicator("All in One Polvitos LUIGI"
  , overlay          = true
  , max_bars_back    = 500
  , max_lines_count  = 500
  , max_boxes_count  = 500
  , max_labels_count = 500)
//------------------------------------------------------------------------------
//Settings
//-----------------------------------------------------------------------------{

Tokyo = input.bool(false, "Activar/Desactivar Cuadradito MM")


//STOP HUNT
show_sese = input(false, 'Activar/Desactivar Stop Hunt'
  , inline = 'sesa'
  , group = 'STOP HUNT RANGE')

sese_txt = input('STOP HUNT RANGE', ''
  , inline = 'sesa'
  , group = 'STOP HUNT RANGE')

sese_ses = input.session('0000-0805', ''
  , inline = 'sesa'
  , group = 'STOP HUNT RANGE')

sese_css = input.color(#0026ff, ''
  , inline = 'sesa'
  , group = 'STOP HUNT RANGE')

sese_range = input(true, 'Range'
  , inline = 'sesa_overlays'
  , group = 'STOP HUNT RANGE')






//Session A
show_sesa = input(true, ''
  , inline = 'sesa'
  , group = 'New York')

sesa_txt = input('New York', ''
  , inline = 'sesa'
  , group = 'New York')

sesa_ses = input.session('1300-2205', ''
  , inline = 'sesa'
  , group = 'New York')

sesa_css = input.color(#0026ff, ''
  , inline = 'sesa'
  , group = 'New York')

sesa_range = input(true, 'Range'
  , inline = 'sesa_overlays'
  , group = 'New York')


//Session B
show_sesb = input(true, ''
  , inline = 'sesb'
  , group = 'London')

sesb_txt = input('London', ''
  , inline = 'sesb'
  , group = 'London')

sesb_ses = input.session('0700-1305', ''
  , inline = 'sesb'
  , group = 'London')

sesb_css = input.color(#f32121, ''
  , inline = 'sesb'
  , group = 'London')

sesb_range = input(true, 'Range'
  , inline = 'sesb_overlays'
  , group = 'London')



//Session C
show_sesc = input(true, ''
  , inline = 'sesc'
  , group = 'Asia')

sesc_txt = input('Asia', ''
  , inline = 'sesc'
  , group = 'Asia')

sesc_ses = input.session('0100-0705', ''
  , inline = 'sesc'
  , group = 'Asia')

sesc_css = input.color(#00ad00, ''
  , inline = 'sesc'
  , group = 'Asia')

sesc_range = input(true, 'Range'
  , inline = 'sesc_overlays'
  , group = 'Asia')



//Session D
show_sesd = input(true, ''
  , inline = 'sesd'
  , group = 'Sesion de Cierre')

sesd_txt = input('Cierre', ''
  , inline = 'sesd'
  , group = 'Sesion de Cierre')

sesd_ses = input.session('2100-0105', ''
  , inline = 'sesd'
  , group = 'Sesion de Cierre')

sesd_css = input.color(#8a8a8a, ''
  , inline = 'sesd'
  , group = 'Sesion de Cierre')

sesd_range = input(true, 'Range'
  , inline = 'sesd_overlays'
  , group = 'Sesion de Cierre')




//Timezones
tz_incr = input.int(0, 'UTC (+/-)'
  , group = 'Timezone')

use_exchange = input(false, 'Use Exchange Timezone'
  , group = 'Timezone')

//Ranges Options
bg_transp = input.float(90, 'Range Area Transparency'
  , group = 'Ranges Settings')

show_outline = input(true, 'Range Outline'
  , group = 'Ranges Settings')

show_txt = input(true, 'Range Label'
  , group = 'Ranges Settings')


//-----------------------------------------------------------------------------}
//Functions
//-----------------------------------------------------------------------------{
n = bar_index

//Get session average
get_avg(session)=>
    var len = 1
    var float csma = na
    var float sma = na

    if session > session[1]
        len := 1
        csma := close
    
    if session and session == session[1]
        len += 1    
        csma += close
        sma := csma / len
    
    sma

//Get trendline coordinates



get_linreg(session)=>
    var len = 1
    var float cwma  = na
    var float csma  = na
    var float csma2 = na

    var float y1 = na
    var float y2 = na
    var float stdev = na 
    var float r2    = na 

    if session > session[1]
        len   := 1
        cwma  := close
        csma  := close
        csma2 := close * close
    
    if session and session == session[1]
        len   += 1    
        csma  += close
        csma2 += close * close
        cwma  += close * len

        sma = csma / len
        wma = cwma / (len * (len + 1) / 2)

        cov   = (wma - sma) * (len+1)/2
        stdev := math.sqrt(csma2 / len - sma * sma)
        r2    := cov / (stdev * (math.sqrt(len*len - 1) / (2 * math.sqrt(3))))

        y1 := 4 * sma - 3 * wma
        y2 := 3 * wma - 2 * sma

    [y1 , y2, stdev, r2]


//Set line
set_line(session, y1, y2, session_css)=>
    var line tl = na

    if session > session[1]
        tl := line.new(n, close, n, close, color = session_css)

    if session and session == session[1]
        line.set_y1(tl, y1)
        line.set_xy2(tl, n, y2)

//Set session range
get_range(session, session_name, session_css)=>
    var t = 0 
    var max = high
    var min = low
    var box bx = na
    var label lbl = na 
    
    if session > session[1]
        t := time
        max := high
        min := low

        bx := box.new(n, max, n, min
          , bgcolor = color.new(session_css, bg_transp)
          , border_color = show_outline ? session_css : na
          , border_style = line.style_dotted)

        if show_txt
            lbl := label.new(t, max, session_name
              , xloc = xloc.bar_time
              , textcolor = session_css
              , style = label.style_label_down
              , color = color.new(color.white, 100)
              , size = size.small)

    if session and session == session[1]
        max := math.max(high, max)
        min := math.min(low, min)

        box.set_top(bx, max)
        box.set_rightbottom(bx, n, min)

        if show_txt
            label.set_xy(lbl, int(math.avg(t, time)), max)

//-----------------------------------------------------------------------------}
//Sessions
//-----------------------------------------------------------------------------{
tf = timeframe.period

var tz = use_exchange ? syminfo.timezone :
  str.format('UTC{0}{1}', tz_incr >= 0 ? '+' : '-', math.abs(tz_incr))

is_sesa = math.sign(nz(time(tf, sesa_ses, tz)))
is_sesb = math.sign(nz(time(tf, sesb_ses, tz)))
is_sesc = math.sign(nz(time(tf, sesc_ses, tz)))
is_sesd = math.sign(nz(time(tf, sesd_ses, tz)))
is_sese = math.sign(nz(time(tf, sese_ses, tz)))

//-----------------------------------------------------------------------------}
//Overlays
//-----------------------------------------------------------------------------{
//Ranges
if show_sesa and sesa_range
    get_range(is_sesa, sesa_txt, sesa_css)

if show_sesb and sesb_range
    get_range(is_sesb, sesb_txt, sesb_css)

if show_sesc and sesc_range
    get_range(is_sesc, sesc_txt, sesc_css)

if show_sesd and sesd_range
    get_range(is_sesd, sesd_txt, sesd_css)

if show_sese and sese_range
    get_range(is_sese, sese_txt, sese_css)

//






//CUADRADITO MM





bgColor = input.bool(true,"")



AsiaColor = color.new(#7fd410, 31)


///Sessions

res = input.timeframe("W", "Resolution", ["D","W","M"])


tokyo = input.session("1600-0005:1", "New York Time preset")


//Bars

is_newbar(sess) =>
    t = time(res, sess, "America/New_York")
    na(t[1]) and not na(t) or t[1] < t

is_session(sess) =>
    not na(time(timeframe.period, sess, "America/New_York"))
    


//Tokyo



tokyoNewbar = is_newbar(tokyo)
tokyoSession = is_session(tokyo)

float tokyoLow = na
tokyoLow := if tokyoSession
    if tokyoNewbar
        low
    else
        math.min(tokyoLow[1],low)
else
    tokyoLow

float tokyoHigh = na
tokyoHigh := if tokyoSession
    if tokyoNewbar
        high
    else
        math.max(tokyoHigh[1],high)
else
    tokyoHigh


plotTL = plot(tokyoLow, color=color.new(#e03030, 100))
plotTH = plot(tokyoHigh, color=color.new(#000000, 100))
fill(plotTL, plotTH, color = tokyoSession and Tokyo and bgColor ? AsiaColor : na)

bgcolor(tokyoSession and Tokyo and not bgColor ? AsiaColor : na)






