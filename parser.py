


from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import requests
import json
import sys

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
		

classes = { "Death Knight": "1", "Druid": "2", "Hunter": "3", "Mage": "4", "Monk": "5", "Paladin": "6", "Priest": "7", "Rogue": "8", "Shaman": "9", "Warlock": "10", "Warrior": "11" }
specs = { "Blood": "1", "Frost": "2", "Unholy": "3", "Balance": "1", "Feral": "2", "Guardian":"3", "Restoration":"4", "Beast Mastery":"1", "Marksmanship":"2", "Survival":"3", "Arcane":"1", "Fire":"2", "Frost":"3", "Brewmaster":"1", "Mistweaver":"2", "Windwalker":"3", "Holy":"1", "Protection_Paladin":"2", "Retribution":"3", "Discipline":"1", "Holy":"2", "Shadow":"3", "Assassination":"1", "Combat": "2", "Subtlety":"3", "Elemental":"1", "Enhancement":"2", "Restoration":"3", "Affliction":"1","Demonology":"2", "Destruction":"3", "Arms":"1", "Fury": "2", "Protection_Warrior":"3", "Gladiator":"4" }

encounters = { "Hellfire Assault": "1778", "Iron Reaver":"1785", "Kormrok": "1787", "Hellfire High Council": "1798", "Kilrogg Deadeye": "1786", "Gorefiend":"1783", "Shadow-Lord Iskar":"1788", "Fel Lord Zakuun":"1777", "Xhul'horac":"1800", "Socrethar the Eternal":"1794", "Tyrant Velhari":"1784", "Mannoroth": "1795", "Archimonde":"1799"  }


tank_classes = {"Death Knight":"Blood", "Druid":"Guardian", "Monk":"Brewmaster", "Paladin":"Protection_Paladin", "Warrior":"Protection_Warrior"}

api_key = "b3a3c2ec50990fbf5a7f10ca5cbd6d4c"
api_url = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"
limit = 10
		
def get_reports_for_spec(tank, spec, encounter_id):
	
	class_id = classes[tank]
	spec_id = specs[spec]
	
	req_url = api_url + encounter_id + "?metric=dps&difficulty=5&class=" + class_id + "&spec=" + spec_id + "&api_key=" + api_key + "&limit=" + str(limit)
	c = requests.get(req_url)
	j = c.json()
	
	ranks = j["rankings"]
	reports = []
	for r in ranks:
		#uprint(r["reportID"], r["fightID"])
		report_url = "https://www.warcraftlogs.com/reports/" + r["reportID"] + "#fight=" + str(r["fightID"]) + "&type=damage-taken&options=34"
		#uprint(report_url, r["name"])
		reports.append((report_url, r["name"]))
	
	return reports

		
def main():


#	u = "https://www.warcraftlogs.com/reports/yZjCXz1gFcRrGdfB#fight=23&type=damage-taken&options=34"
#	browser = Firefox()
	
#	browser.get(u)
#	playername = "Trolden"
#	WebDriverWait(browser, timeout=10).until(lambda x: x.find_element_by_id('main-table-0'))
	#tabl = browser.find_element_by_xpath("//table[@id='main-table-0']")
	#print(tabl.text)
	#test = browser.find_element_by_xpath("//*[contains(text(),'"+playername+"')]::ancestor")
	#test = browser.find_element_by_xpath("//table[@id='main-table-0']/*[text()[contains(.,'"+playername+"')]]")
	#test = browser.find_element_by_xpath("//tr[@role='row' and text()[contains(.,'"+playername+"')]]")
#	test = browser.find_element_by_xpath("//*[text()[contains(.,'"+playername+"') ] ]/ancestor::tr[@role='row']")
#	data = test.text.split('\n')
#	damage_taken = data[2]
#	print(playername, " took", damage_taken, "total damage")
	#print(test)
	#print(type(test))
	#print(test.tag_name)
	#print("text:",test.text)
			
#	return



	
	
	
	#    https://www.warcraftlogs.com/reports/f2HcPkqtn9JxbT4z#fight=3&type=damage-taken
	
	class_reports = {}
	
	for tank, spec in tank_classes.items():
		#print(tank, spec)
		print("getting reports for",tank, spec)
		report = get_reports_for_spec(tank, spec, encounters["Fel Lord Zakuun"])
		class_reports[tank] = report
		
#	print("done")
#	for _class, reports in class_reports.items():
#		print("reports for", _class)
#		for r in reports:
#			uprint(r)

	log = open("log.txt", "w")
	result = open("result.txt", "w")

	dmgtotal_logs = {"Death Knight": [], "Druid":[], "Monk":[], "Paladin":[], "Warrior":[]}
	dtps_logs = {"Death Knight": [], "Druid":[], "Monk":[], "Paladin":[], "Warrior":[]}
	
	browser = Firefox()
	for _class, reports in class_reports.items():
		print("checking reports for", _class)
		cur_report = 0
		for r in reports:
			#uprint("report", cur_report, r)
			#log.writeline("report " + str(cur_report) +" "+ r[0] + " " + r[1])
			uprint("report", cur_report, r)
			uprint("report", cur_report, r, file=log)
			url = r[0]
			playername = r[1]
			browser.get("about:blank")
			browser.get(url)
			WebDriverWait(browser, timeout=20).until(lambda x: x.find_element_by_id('main-table-0'))
			
			row = browser.find_element_by_xpath("//*[text()[contains(.,'"+playername+"') ] ]/ancestor::tr[@role='row']")
			data = row.text.split('\n')
			damage_taken = data[2]
			dtps = data[3].split(" ")[3]
			dtps = dtps.replace(",","")
			#log.write(playername +" " + damage_taken +" "+ dtps)
			uprint(playername, damage_taken, dtps)
			uprint(playername, damage_taken, dtps, file=log)
			if damage_taken[-1] != "m":
				print("< 1m damage taken, skipping")
				continue
			#print(float(damage_taken[:-1]), float(dtps))
			dt_tot = float(damage_taken[:-1])
			dtpsf = float(dtps)
			dmgtotal_logs[_class].append(dt_tot)
			dtps_logs[_class].append(dtpsf)
			
			#test.screenshot("foo.png")
			#f.write(str(idx))
				
				
			cur_report += 1

	

	class_to_total = {"Death Knight": 0.0, "Druid":0.0, "Monk":0.0, "Paladin":0.0, "Warrior":0.0}
	class_to_totalavg = {"Death Knight": 0.0, "Druid":0.0, "Monk":0.0, "Paladin":0.0, "Warrior":0.0}
	class_to_dtps = {"Death Knight": 0.0, "Druid":0.0, "Monk":0.0, "Paladin":0.0, "Warrior":0.0}
	class_to_dtpsavg = {"Death Knight": 0.0, "Druid":0.0, "Monk":0.0, "Paladin":0.0, "Warrior":0.0}
	
	for key, val in dmgtotal_logs.items():
		total_damage_taken = sum(val)
		avg_damage_taken = total_damage_taken / len(val)
		class_to_total[key] = total_damage_taken
		class_to_totalavg[key] = avg_damage_taken
	
	for key, val in dtps_logs.items():
		total_damage_taken = sum(val)
		avg_damage_taken = total_damage_taken / len(val)
		class_to_dtps[key] = total_damage_taken
		class_to_dtpsavg[key] = avg_damage_taken
		
	for key,value in class_to_total.items():
		uprint(key, "total:", class_to_total[key], "avg:", class_to_totalavg[key], "total_dtps:",class_to_dtps[key],"dtps_avg:",class_to_dtpsavg[key])
		uprint(key, "total:", class_to_total[key], "avg:", class_to_totalavg[key], "total_dtps:",class_to_dtps[key],"dtps_avg:",class_to_dtpsavg[key], file=result)
		uprint(key, "total:", class_to_total[key], "avg:", class_to_totalavg[key], "total_dtps:",class_to_dtps[key],"dtps_avg:",class_to_dtpsavg[key], file=log)
	
	
	log.close()
#	with closing(Firefox()) as browser:
#		browser.get(url)
#		#button = browser.find_element_by_name('button')
#		#button.click()
#		# wait for the page to load
#		WebDriverWait(browser, timeout=10).until(lambda x: x.find_element_by_id('table-container'))
#		# store it to string variable
#		page_source = browser.page_source
#		#print(page_source)
#		idx = page_source.find("Hell")
#		print(idx)
#		f.write(str(idx))
#		f.close()
#	#print()
	

	
	
	
	
	
	
	
	
	
	
	#	api_url = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"
#	encounter_id = "1777"
#	class_id = classes["Death Knight"]
#	spec_id = "1"
#	req_url = api_url + encounter_id + "?metric=dps&difficulty=5&class=" + class_id + "&spec=" + spec_id + "&api_key=" + api_key
#	c = requests.get(req_url)
#	j = c.json()
	
#	ranks = j["rankings"]
#	reports = []
#	for r in ranks:
#		#uprint(r["reportID"], r["fightID"])
#		report_url = "https://www.warcraftlogs.com/reports/" + r["reportID"] + "#fight=" + str(r["fightID"]) + "&type=damage-taken"
#		#uprint(report_url, r["name"])
#		reports.append(report_url)
	
#	for r in reports:
#		print(r)
	
#	return
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main()