import soundcard as sc
import soundfile as sf
import speech_recognition as sr
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def bypasscaptchaV2(driver, submit, iframe):
    arquivo_audio = "recaptcha_"+str(datetime.now().strftime("%Y-%m-%d_%H-%M"))+".wav"
    sample_rate = 48000
    segundos = 5

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, submit))).click()
    driver.switch_to.frame( WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, iframe))))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "recaptcha-audio-button"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'REPRODUZIR')]"))).click()

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
        data = mic.record(numframes=sample_rate * segundos)
        sf.write(file=arquivo_audio, data=data[:, 0], samplerate=sample_rate)

    r = sr.Recognizer()
    with sr.AudioFile(arquivo_audio) as source:
        audio = r.record(source, duration=segundos)
        text = r.recognize_google(audio, language='en-US', show_all=True)
        try:
            print(' > Resposta: ', text['alternative'][0]['transcript'])
            driver.find_element(By.ID, "audio-response").send_keys(text['alternative'][0]['transcript'])
            driver.find_element(By.XPATH, "//button[contains(.,'Verificar')]").click()
            return True
        except: return False






