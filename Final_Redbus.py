import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, Column, String, Integer, Time, Numeric, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

  
def web_scraping(src, dest,user_yr, user_mon, day):
    driver = webdriver.Chrome()
    driver.get('https://www.redbus.in/');   #---> change url to whatever website to scrape from
    
    time.sleep(5)     #---> giving time for page to load before executing the next line of code
    
    driver.find_element(By.ID, 'src').send_keys(src)
    time.sleep(2)   #----> needed for it to load teh dropdowns
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()
    
    driver.find_element(By.ID, 'dest').send_keys(dest)
    time.sleep(2)   #----> needed for it to load teh dropdowns
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()
    
    time.sleep(2)                           #---> giving time for page to load before executing the next line of code
    
    driver.find_element(By.ID, "onwardCal").click()
    date = driver.find_element(By.CSS_SELECTOR, "div[style='flex-grow: 2; font-size: 0.875rem;']")
    date = str(date.text)
    date = date.split()

    
    time.sleep(2)
    
    #left_arr = driver.find_element(By.XPATH,"/html/body/section/div[2]/main/div[3]/div[1]/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[1]")
    right_arr = driver.find_element(By.XPATH,"/html/body/section/div[2]/main/div[3]/div[1]/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[3]")
    
    red_yr = int(date[1])
    
    while red_yr != int(user_yr):
        right_arr.click()
        time.sleep(1)
        date = driver.find_element(By.CSS_SELECTOR, "div[style='flex-grow: 2; font-size: 0.875rem;']")
        date = str(date.text)
        date = date.split()
        red_yr = int(date[1])
        time.sleep(1)
    
    red_mon = date[0]
    red_mon_num = {'Jan': 1,'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,'Sep': 9, 'Oct': 10, 'Nov': 11,'Dec': 12}[red_mon]
    user_mon_num = {'Jan': 1,'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,'Sep': 9, 'Oct': 10, 'Nov': 11,'Dec': 12}[user_mon]
    
    while red_mon_num != user_mon_num:
        right_arr.click()
        time.sleep(1)
        date = driver.find_element(By.CSS_SELECTOR, "div[style='flex-grow: 2; font-size: 0.875rem;']")
        date = str(date.text)
        date = date.split()
        red_mon = str(date[0])
        red_mon_num = {'Jan': 1,'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,'Sep': 9, 'Oct': 10,'Nov': 11,'Dec': 12}[red_mon]
        time.sleep(1)
    
    driver.find_element(By.XPATH,"//div[@class='DayTiles__CalendarDaysBlock-sc-1xum02u-0 isgDNj']/span[text()='"+ str(day)+"']").click()
    
    driver.find_element(By.ID,"search_button").click()
    time.sleep(5)

    no_buses = driver.find_element(By.CSS_SELECTOR, "span[class='f-bold busFound']")
    text= (no_buses.text)
        
    ind = 0
    num = []
    while text[ind] != ' ':
        num.append(text[ind])
        ind+=1
        
    no_of_buses = int("".join(num))    
        
    scrolling = 0
    while scrolling < no_of_buses:
        
        body=driver.find_element(By. TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)
            
        time.sleep(2)
            
        bname = driver.find_elements (By.CSS_SELECTOR, "div[class = 'travels lh-24 f-bold d-color']")
        scrolling = len(bname)
        
    
    src = driver.find_elements (By.CSS_SELECTOR, "div[class='column-three p-right-10 w-10 fl']")
    dest = driver.find_elements (By.CSS_SELECTOR, "div[class='column-five p-right-10 w-10 fl']")
    
    bname = driver.find_elements (By.CSS_SELECTOR, "div[class = 'travels lh-24 f-bold d-color']")
    btype = driver.find_elements (By.CSS_SELECTOR, "div[class = 'bus-type f-12 m-top-16 l-color evBus']")
    dep_time = driver.find_elements (By.CSS_SELECTOR, "div[class = 'dp-time f-19 d-color f-bold']")
    dur = driver.find_elements (By.CSS_SELECTOR, "div[class = 'dur l-color lh-24']")
    reach_time = driver.find_elements (By.CSS_SELECTOR, "div[class = 'bp-time f-19 d-color disp-Inline']")
    star_rat = driver.find_elements (By.CSS_SELECTOR, "div[class='rating-sec lh-24']")
    
    pric = driver.find_elements (By.CSS_SELECTOR, "div[class='seat-fare ']")
    
    sts = driver.find_elements (By.CSS_SELECTOR, "div[class='column-eight w-15 fl']")

    
    ID = []
    SOURCE = []
    DEST = []
    BUS_NAME = []
    BUS_TYPE = []
    DEPARTING_TIME = []
    DURATION = []
    REACHING_TIME = []
    STAR_RATING = []
    PRICE = []
    SEATS = []
    LINK = []
    
    def create_list(name,list):
        for i in name:
            list.append(i.text)

    for i in src:
        i = i.text
        i = i.split('\n',2)[1]
        SOURCE.append(i)
    
    
    for i in dest:
        i = i.text
        i = i.split('\n',2)[-1]
        DEST.append(i)
        
    create_list(bname, BUS_NAME)
    create_list(btype, BUS_TYPE)
    create_list(dep_time, DEPARTING_TIME)
    create_list(dur, DURATION)
    create_list(reach_time, REACHING_TIME)
    create_list(star_rat, STAR_RATING)

    for i in range(len(SOURCE)):
        ID.append(i+1)

    new_url = driver.current_url
    for i in range(len(SOURCE)):
        LINK.append(new_url)
        
    for i in pric:
        i.get_attribute('span')
        i = i.text.split(' ')
        for j in i:
            try:
                PRICE.append(int(j))
                break
            except:
                continue

    for i in sts:
        i = i.text
        i = i.split(' ')[0]
        SEATS.append(int(i))

    data = [ID,SOURCE, DEST, BUS_NAME, BUS_TYPE, DEPARTING_TIME, DURATION, REACHING_TIME, STAR_RATING, PRICE, SEATS, LINK]
    
    busdf=pd.DataFrame(data).T
    busdf.columns=['ID','SOURCE', 'DEST','BUS_NAME', 'BUS_TYPE', 'DEPARTING_TIME', 'DURATION', 'REACHING_TIME','STAR_RATING', 'PRICE', 'SEATS', 'LINK']

    def replace_values(val):
        if 'non'.lower() in val.lower():
            if 'seater/sleeper'.lower() in val.lower():
                return 'Non-AC,Seater,Sleeper'
            elif 'sleeper/seater'.lower() in val.lower():
                return 'Non-AC,Seater,Sleeper'
            elif 'sleeper'.lower() in val.lower():
                return 'Non-AC,Sleeper'
            else:
                return 'Non-AC,Seater'
        else:
            if 'seater/sleeper'.lower() in val.lower():
                return 'AC,Seater,Sleeper'
            elif 'sleeper/seater'.lower() in val.lower():
                return 'AC,Seater,Sleeper'
            elif 'sleeper'.lower() in val.lower():
                return 'AC,Sleeper'
            else:
                return 'AC,Seater'
    
    busdf['BUS_TYPE'] = busdf['BUS_TYPE'].str.replace(' ', '')
    busdf['BUS_TYPE'] = busdf['BUS_TYPE'].map(replace_values)

    BUS_DATA = busdf
    driver.quit()

    return BUS_DATA

def SQL_filter(BUS_DATA, AC_NonAC, Seat_Sleep):
    metadata = MetaData()
    Base = declarative_base(metadata=metadata)

    class REDBUS(Base):
        
        __tablename__ = 'redbus_final'

        id = Column('id', Integer, primary_key=True)
        source = Column('source', String(255))
        dest = Column('dest', String(255))
        bus_name = Column('bus_name', String(255))
        bus_type = Column('bus_type', String(255))
        departing_time = Column('departing_time', Time)
        duration = Column('duration', String(255))
        reaching_time = Column('reaching_time', Time)
        star_rating = Column('star_rating', Float)
        price = Column('price', Numeric(10,2))
        seats = Column('seats', Integer)
        link = Column('link', String(255))


        def __init__(self, id, source, dest, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats, link):
            self.id = id
            self.source = source
            self.dest = dest
            self.bus_name = bus_name
            self.bus_type = bus_type
            self.departing_time = departing_time
            self.duration = duration
            self.reaching_time = reaching_time
            self.star_rating = star_rating
            self.price = price
            self.seats = seats
            self.link = link

        def __repr__(self):
            return f"({self.id}) {self.source} {self.dest} {self.bus_name} {self.bus_type} {self.departing_time} {self.duration} {self.reaching_time} ({self.star_rating}, {self.price}, {self.seats}, {self.link})"


    engine = create_engine("mysql+pymysql://root:195524@localhost:3306/redbus", echo=True)

    #Base.metadata.create_all(bind=engine)

    # Drop table if exists
    metadata.drop_all(engine)

    # Create table defined in the metadata
    metadata.create_all(engine)

    
    Session = sessionmaker(bind=engine)
    session = Session()


    for i in range(len(BUS_DATA)):
        row = list(BUS_DATA.iloc[i])
        bus = REDBUS( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
        session.add(bus)

    if AC_NonAC == 'AC' and Seat_Sleep == 'Seater':
        results = session.query(REDBUS).filter(REDBUS.bus_type.in_(["AC,Seater,Sleeper", "AC,Seater"])).all()
    elif AC_NonAC == 'AC' and Seat_Sleep == 'Sleeper':
        results = session.query(REDBUS).filter(REDBUS.bus_type.in_(["AC,Seater,Sleeper", "AC,Sleeper"])).all() #AC buses
    elif AC_NonAC == 'Non-AC'and Seat_Sleep == 'Seater':
        results = session.query(REDBUS).filter(REDBUS.bus_type.in_(['Non-AC,Seater,Sleeper', 'Non-AC,Seater'])).all() 
    elif AC_NonAC == 'Non-AC'and Seat_Sleep == 'Sleeper':
        results = session.query(REDBUS).filter(REDBUS.bus_type.in_(['Non-AC,Seater,Sleeper', 'Non-AC,Sleeper'])).all() #Non AC buses


    data = []
    for product in results:
        data.append({
            'ID': product.id,
            'Source': product.source,
            'Dest': product.dest,
            'Bus Name': product.bus_name,
            'Bus Type': product.bus_type,
            'Departing Time': product.departing_time,
            'Duration': product.duration,
            'Reaching Time': product.reaching_time,
            'Rating': product.star_rating,
            'Price': product.price,
            'Seats': product.seats,
            'Link': product.link
        })
    df = pd.DataFrame(data)
    
    session.commit()
    return df


def filter_buses(df, price, rating, seat):
    
    # Filter for star rating
    df = df[df['Rating'] >= rating]
    
    # Filter for price
    df = df[df['Price'] <= price]
    
    # Filter for seats
    df = df[df['Seats'] >= int(seat)]
    df["Link"] = df["Link"].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    return df


def main():
    st.title('RedBus Online Booking')

    src = st.sidebar.text_input('Pick-up City/Town: ')
    dest = st.sidebar.text_input('Destination City/Town: ')
    user_yr = st.sidebar.selectbox('Year',('2024','2025','2026','2027','2028','2029','2030','2031','2032','2033','2034','2035'))
    user_mon = st.sidebar.selectbox('Month',('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))

    if user_mon == 'Jan' or user_mon == 'Mar' or user_mon == 'May' or user_mon == 'Jul' or user_mon == 'Aug' or user_mon == 'Oct' or user_mon == 'Dec':
        day = st.sidebar.selectbox('Date',("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"))
    elif user_mon == 'Feb' and int(user_yr)%4 == 0:
        day = st.sidebar.selectbox('Date',("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"))
    elif user_mon =='Feb' and int(user_yr)%4 != 0:
        day = st.sidebar.selectbox('Date',("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"))
    else:
        day = st.sidebar.selectbox('Date',("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"))
    
    
    AC_NonAC = st.selectbox('AC/ Non AC', ('AC', 'Non-AC'))
    Seat_Sleep = st.selectbox('Seater/ Sleeper',('Seater', 'Sleeper'))
    price = float(st.slider('Price',min_value=0, max_value=10000, step=50))
    rating = float(st.slider('Rating',min_value=0.0, max_value=5.0, step = 0.1))
    seat = st.text_input('No of Seats booked: ')

    search = st.button('Search Buses')
    
    if search:
        dataframe = web_scraping(src, dest,user_yr, user_mon, day)
        SQL_data = SQL_filter(dataframe, AC_NonAC, Seat_Sleep)
        final = filter_buses(SQL_data, price, rating, seat)
        st.write(
            final.to_html(escape=False, index=False),  # Render HTML, disable escaping
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
