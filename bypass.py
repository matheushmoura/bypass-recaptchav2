import soundcard as sc
import soundfile as sf
import speech_recognition as sr
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
sample_rate = 48000

def gravar_audio_captcha(arquivo_audio, sample_rate, segundos):
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
        data = mic.record(numframes=sample_rate * segundos)
        sf.write(file=arquivo_audio, data=data[:, 0], samplerate=sample_rate)

def audio_para_texto_captcha(arquivo_audio, segundos):
    r = sr.Recognizer()
    with sr.AudioFile(arquivo_audio) as source:
        audio = r.record(source, duration=segundos)
        text = r.recognize_google(audio, language='en-US', show_all=True)
        return text

def bypasscaptchaV2(driver, submit_selector, iframe_selector):
    arquivo_audio = "recaptcha_"+str(datetime.now().strftime("%Y-%m-%d_%H-%M"))+".wav"
    segundos = 5
    nao_resolveu_captcha = True

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, submit_selector))).click()
    driver.switch_to.frame( WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, iframe_selector))))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "recaptcha-audio-button"))).click()

    while nao_resolveu_captcha:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'REPRODUZIR')]"))).click()
        gravar_audio_captcha(arquivo_audio, sample_rate, segundos)
        text = audio_para_texto_captcha(arquivo_audio, segundos)
        try:
            print(' > Resposta: ', text['alternative'][0]['transcript'])
            driver.find_element(By.ID, "audio-response").send_keys(text['alternative'][0]['transcript'])
            driver.find_element(By.XPATH, "//button[contains(.,'Verificar')]").click()
            try:
                # Mensagem de erro
                print(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='rc-audiochallenge-error-message']"))).text)
                driver.find_element(By.XPATH, "//button[@id='recaptcha-reload-button']").click()
            except:
                # Resolveu
                return True
        except:
            # Não conseguiu resolver
            driver.find_element(By.XPATH, "//button[@id='recaptcha-reload-button']").click()





