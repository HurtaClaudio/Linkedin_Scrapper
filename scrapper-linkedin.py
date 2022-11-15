from variables_imports import *
from funciones_importantes import revisar_pais_latino, scrollear_al_job, read_keys_from_txt

geolocator = Nominatim(user_agent = "geoapiExercises")
warnings.filterwarnings("ignore")

print("Iniciamos webdriver")
### Corrida CHROME

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
#options.add_argument('headless')
options.add_argument('no-sandbox')
print("Establecemos opciones.")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
df = pd.DataFrame(columns=['Job_description', 'Company', 'Job_offer_url', 'Nro_empleados', 'Empleados_latinos', 'Porcentaje_latinos', 'Hires_latinos', 'N_hires_dict'])


keys = read_keys_from_txt()

# Ingresamos al portal
url = 'https://www.linkedin.com'
driver.get(url)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='sign-in-form__submit-button']")))

# ponemos las credenciales

# Mail
mail_str = keys['user']
mail = driver.find_element(By.XPATH, "//input[@id='session_key']")
mail.clear()
mail.send_keys(mail_str)
time.sleep(.2)



# Contraseña
psw_str = keys['pass']
psw = driver.find_element(By.XPATH, "//input[@id='session_password']")
psw.clear()
psw.send_keys(psw_str)
time.sleep(.2)


# Presionamos botón de inicio
boton_actuales = driver.find_element(By.XPATH, "//button[@class='sign-in-form__submit-button']")
action = ActionChains(driver)
action.move_to_element(boton_actuales)
action.click().perform()
print('Presionamos botón de incio de sesión')

#Esperamos a que cargue la pagina
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='ember28']")))



# Ponemos la query de empleo
# Data scientist
url_job_query =  'https://www.linkedin.com/jobs/search/?currentJobId=3352950777&distance=25&f_AL=true&f_E=4&f_SB2=1&f_TPR=r86400&f_WT=2&geoId=103644278&keywords=data%20scientist&sortBy=R'

# ML Engineer
#url_job_query = 'https://www.linkedin.com/jobs/search/?currentJobId=3357244907&f_AL=true&f_E=2%2C3%2C4&f_SB2=2&f_TPR=r86400&f_WT=2&keywords=machine%20learning%20engineer&refresh=true&sortBy=R'

driver.get(url_job_query)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mostrar todos los filtros. Al hacer clic en este botón, se muestran todas las opciones de filtros disponibles.']")))



# Aqui empieza el for loop, son 25 elementos por pagina, y son 2 paginas
#recorremos las job offers
job_offers = 25
for nro_job in range(1, job_offers + 1):
    print(f'Escrapeando job posting nro {nro_job}.')

    # Ante cualquier error inesperado seguimos con el siguiente perfil
    try:
        scrollear_al_job(driver, nro_job)

        #recuperamos cada trabajo individual
        try:
            job_offer = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[1]/a')
            company = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[2]/a')[0].text
        except:
            job_offer = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[1]/a')
            company = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[2]/a')[0].text

        job_link = job_offer[0].get_attribute('href')
        job_description = job_offer[0].text
        print(company)
        print(job_description)


        #nos metemos a la pagina de personas de la compañia en una nueva ventana
        try:
            try:                                                          
                company_url = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[2]/a')[0].get_attribute('href')
            except:
                company_url = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[1]/a')[0].get_attribute('href')
        except:
            try:
                company_url = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[2]/a')[0].get_attribute('href')
            except:
                company_url = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{nro_job}]/div/div[1]/div[1]/div[2]/div[1]/a')[0].get_attribute('href')


        # Cargamos la pagina de personas
        driver.get(company_url + 'people/')
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Añade una ubicación']")))

        # Recuperamos el numero de empleados
        nro_empleados = driver.find_elements(By.XPATH, '//h2[@class="t-20 t-black t-bold"]')[0].text
        nro_empleados = nro_empleados[:nro_empleados.find(' ')]
        nro_empleados = nro_empleados.replace('.', '')
        nro_empleados = int(nro_empleados)
        print(f'Nro empleados compañia: {nro_empleados}.')

        # recuperamos la lista de las ubicaciones
        employee_locations_html = driver.find_elements(By.XPATH, '//div[@class="insight-container"]')[0]

        # siempre son 5 ubicaciones por default
        employees_dict = {}
        for i in range(5):
            employee_location =  employee_locations_html.find_elements(By.XPATH, '//button[@class="org-people-bar-graph-element mt2 text-align-left full-width org-people-bar-graph-element--is-selectable "]')[i].text
            #removemos ' y alrededores'
            employee_location = employee_location.replace(' y alrededores', '')

            #extraemos los datos
            location = employee_location[employee_location.find(' '):].strip()
            n = employee_location[:employee_location.find(' ')]
            n = n.replace('.', '')
            n = int(n)
            print(location, n)
            # ahora sí! usamos la API
            location_api = geolocator.geocode(location)[0]
            last_comma_idx = len(location_api) - location_api[::-1].find(',')

            if last_comma_idx != len(location_api) + 1:
                location = location_api[last_comma_idx:].strip()
            else:
                location = location_api

            # Sumamos los empleados al diccionario
            try:
                # Tratamos de agregar si esque ya está el país en la lista
                employees_dict[location] += n
            except:
                # si no está, lo incluimos
                employees_dict[location] = n


        #agregamos un loop para buscar en paises latinos.
        paises_latinos = ['chile', 'argentina', 'peru', 'colombia', 'ecuador', 'brasil', 'venezuela', 'costa rica', 'cuba', 'mexico']
        paises_latinos = {pais: 0 for pais in paises_latinos}
        for pais_latino in paises_latinos.keys():

            try:
                revisar_pais_latino(driver, pais_latino, paises_latinos)
            except Exception as error:
                #volvemos a cargar la pagina y saltamos al siguiente país
                print('hubo error en la pestaña people')
                print(error)
                driver.get(company_url + 'people/')
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Añade una ubicación']")))
                continue

        
        # Finalmente revisamos si es que el trabajo contrata latinos.
        job_hires_latinos = False


        # Revisamos los resultados latinos
        empleados_latinos = 0
        for key,value in paises_latinos.items():
            if value > 0:
                job_hires_latinos = True
                empleados_latinos += value

        # Revisamos los resultados nativos
        for key,value in employees_dict.items():
            if (key.lower() in paises_latinos.keys()) and (value > 0):
                job_hires_latinos = True

        # Hacemos check final
        if job_hires_latinos:
            print('Empresa contrata latinos! ')
        else:
            print('Empresa contrata puro primer mundo.')
        print('')

        # volvemos a la pagina de inicio
        driver.get(url_job_query)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mostrar todos los filtros. Al hacer clic en este botón, se muestran todas las opciones de filtros disponibles.']")))
       

        job_info = [job_description, company, job_link, nro_empleados, empleados_latinos, 
            int((empleados_latinos / nro_empleados) * 100), job_hires_latinos, paises_latinos]

        df.loc[len(df)] = job_info
    
    except Exception as error:
        # Reportamos el error..
        print('Hubo error en lugar no identificado.')
        print(error)

        # Volvemos a la página de inicio..
        driver.get(url_job_query)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mostrar todos los filtros. Al hacer clic en este botón, se muestran todas las opciones de filtros disponibles.']")))

        # y continuamos.
        continue

fecha_scrapeo = str(date.today())
df = df.query('Hires_latinos == True')
df.drop(columns=['Hires_latinos'], inplace=True)
df.to_excel(f'jobs/jobs_{fecha_scrapeo}.xlsx', index=False)

# Logs finales
print('')
print('Escrapeo finalizado.')


