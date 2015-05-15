#!/usr/bin/env python2.7

import selenium
from selenium import webdriver
from selenium import common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
import openpyxl
import xlsxwriter

def data_scrape(url): 

	teams = ['home','away']
	types = {'summary': '1', 'defensive': '3', 'offensive': '2', 'passing': '4'}
	driver = webdriver.PhantomJS(executable_path=r"C:\phantomjs-2.0.0-windows\bin\phantomjs.exe", service_log_path=os.path.devnull, service_args=['--ignore-ssl-errors=true', '--proxy-type=None', '--ssl-protocol=tlsv1'])
	wait = WebDriverWait(driver, 30)

	for team in teams:
		for t in types.keys():

			driver.get(url)
			wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="player-table-statistics-body"]/tr/td')))
			button = driver.find_element_by_xpath('//*[@id="live-player-%s-options"]/li[%s]/a' % (team, types[t]))
			button.click()
			time.sleep(5)
			wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="player-table-statistics-body"]/tr/td')))

			sides = driver.find_elements_by_xpath('//h2/a')
			if team == 'home':
				side = sides[0].text
			elif team == 'away':
				side = sides[1].text

			master_data = driver.find_elements_by_xpath('//*[@id="statistics-table-%s-%s"]//tr/td' % (team, t))
			header_data = driver.find_elements_by_xpath('//*[@id="statistics-table-%s-%s"]//tr/th' % (team, t))
			
			header_list = data_to_list(header_data,'header')
			length = len(header_list)

			master_list = data_to_list(master_data,'master')
			master_list = [master_list[x:x+length] for x in range(0, len(master_list) - (length-1), length)]

			globals()['%s_%s_%s_dataframe' % (side,team,t)] = pd.DataFrame(master_list,columns=header_list)
			excel_writer=pd.ExcelWriter('C:\Users\leslie hau\Documents\python\whoscored.xlsx')
			globals()['%s_%s_%s_dataframe' % (side,team,t)].to_excel(excel_writer,sheet_name=['%s_%s_%s_dataframe' % (side,team,t)],engine='xlsxwriter')
			excel_writer.save()
			'''print(globals()['%s_%s_%s_dataframe' % (side,team,t)])                        '''	

	driver.quit()


def data_to_list(data, name):
	globals()['%s_list' % (name)] = []
	for element in data:
		globals()['%s_list' % (name)].append(element.text)
	return globals()['%s_list' % (name)]


def main():
	print('running')
	url = 'http://www.whoscored.com/Matches/829813/LiveStatistics/England-Premier-League-2014-2015-Aston-Villa-Queens-Park-Rangers'
	data_scrape(url)


if __name__ == '__main__':
   main()
