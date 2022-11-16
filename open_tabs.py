from variables_imports import *
from funciones_importantes import *

fecha_scrapeo = str(date.today())
# O cualquier fecha arbitraria
#fecha_scrapeo = '2022-11-15'

df = pd.read_excel(f'jobs/jobs_{fecha_scrapeo}.xlsx')
urls = df['Job_offer_url']

keys, _ = read_keys_and_jobquery_from_txt()
driver = iniciar_driver()
ingresar_linkedin(driver, keys)


posts = 0
for posts in range(len(urls)):
    print(posts)
    driver.get(urls[posts])    
    if(posts!=len(urls)-1):
       driver.execute_script("window.open('');")
       chwd = driver.window_handles
       driver.switch_to.window(chwd[-1])
       time.sleep(3)

counter = 0
while(True):
    time.sleep(10)
    counter += 1
    if counter % 2 == 0:
        print('Sigo funcionando, espero a que termines.')
    if counter % 2 != 0:
        print('(8) Estoy aqui, queriendote, ahogandome en recuerdos y palabras y.. (8)')
