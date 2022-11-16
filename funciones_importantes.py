from variables_imports import *


def revisar_pais_latino(driver, pais_latino, paises_latinos):
    #hacemos click en el botón
    boton_agregar_pais = driver.find_element(By.XPATH, "//button[@aria-label='Añade una ubicación']")
    action = ActionChains(driver)
    action.move_to_element(boton_agregar_pais)
    time.sleep(.1)
    action.click().perform()
    time.sleep(.1)


    #ingresamos el nombre
    agregar_pais = driver.find_element(By.XPATH, "//input[@id='people-bar-graph-module-facet-search-input']")
    agregar_pais.clear()
    agregar_pais.send_keys(pais_latino)
    time.sleep(1.5)
    agregar_pais.send_keys(Keys.DOWN)
    agregar_pais.send_keys(Keys.ENTER)
    # esperamos a que cargue la pagina
    WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[2]/div/div[1]/div/ul/li[1]/button/span")))


    # obtenemos el numero de empleados
    try:
        n_empleados_pais = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/div[1]/h2").text
        n_empleados_pais = int(n_empleados_pais[:n_empleados_pais.find(' ')])
    except Exception:
        n_empleados_pais = 0


    # Guardamos los resultados
    paises_latinos[pais_latino] = n_empleados_pais

    # apretamos el botón de cerrar
    boton_cerrar = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[2]/div/div[1]/div/ul/li[1]/button/span")
    action = ActionChains(driver)
    action.move_to_element(boton_cerrar)
    action.click().perform()
    print(f'País escrappeado: {pais_latino.title()}, N empleados: {n_empleados_pais}.')
    return None

def scrollear_al_job(driver, nro_job):
    for j in range(1, nro_job, 3):
        try:
            element = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[1]/a')[0]
        except:
            element = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{j}]/div/div[1]/div[1]/div[2]/div[1]/a')[0]

        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(.2)
    return None

def read_keys_and_jobquery_from_txt():
    # To store lines
    keys = {}
    job_query_urls = []
    with open('keys.txt', 'r') as fp:
        for i, line in enumerate(fp):
            # read line 0 and 1
            if i == 0:
                keys['user'] = line.strip()
            elif i == 1:
                keys['pass'] = line.strip()
            else:
                job_query_urls.append(line.strip())
    return keys, job_query_urls

def iniciar_driver():
    print("Iniciamos webdriver")
    ### Corrida CHROME

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    #options.add_argument('headless')
    options.add_argument('no-sandbox')
    print("Establecemos opciones.")
    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

def ingresar_linkedin(driver, keys):
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
    return None

