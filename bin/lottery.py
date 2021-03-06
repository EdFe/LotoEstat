#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Copyright (C) 2011 Alexandre Baaklini, abaaklini@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
from __future__ import print_function
import operator
import matplotlib.pyplot as plt
import utils
import os
import pickle
from parsepage import ParsePage
import numpy as np

class Lottery (object):
    """
    """
    def __init__(self, data_file, sub_table = 0):
        """
        """
        if os.path.exists(self.pickle_file):
            if os.path.getmtime(self.pickle_file) > os.path.getmtime(data_file):
                try:
                    with open(self.pickle_file, 'rb') as data_bin:
                        self.all_content = pickle.load(data_bin)
                        if sub_table > 0:
                            self.all_content = self.all_content[:sub_table]

                except IOError as err:
                    print ("File error: " + str(err))
        else:
            p = ParsePage(self.doz_by_raffle) 
            p.feed(utils.get_content(data_file))
            self.all_content = p.get_full_data()
            if sub_table > 0:
                self.all_content = self.all_content[:sub_table]
            try:
                with open(self.pickle_file, 'wb') as data_bin:
                    pickle.dump(self.all_content, data_bin)

            except IOError as err:
                print ("File error: " + str(err))

        self.all_stat = []
        self.even_odd = {}
        self.doze = {}
        self.even_odd = {'e' + str(i) + 'xo' + str(j): [] for i in range(0, self.doz_by_raffle + 1) for j in reversed(range(0, self.doz_by_raffle + 1))  if (i+j) == self.doz_by_raffle}
        self.doze = {str(i) + 'x': [] for i in range(0, self.dozen_dozens + 1)}
        self.unit = {'x' + str(i): [] for i in range(0, 10)}
        self.init_stat_table()
        self.build_occur_list()
        self.build_delay_list()
        self.build_freq_dict()
        self.more_often_num()
        self.last_time()
        self.most_delay()
        self.aver_delay()
        self.fill_up_stand_dev()
        self.fill_up_stand_sco()
        self.rule_even_by_odd()
        self.more_often_dozen()
        self.more_often_unit()

    def print_more_often_dozen (self):
        """
        """
        di = {str(i) + 'x': len(self.doze[str(i) + 'x']) for i in range(0, self.dozen_dozens + 1) for j in reversed(range(0, self.dozen_dozens + 1))  if (i+j) == self.dozen_dozens}
        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def init_stat_table(self):
        """
        """
        for num in range(1, self.num_dozens + 1):
            self.all_stat.append({'More': 0, 'Last': 0, 'Average': 0, 'Worst': 0, 'Occur': [], 'Delay': [], 'Std_Dev': 0, 'Std_Sco': 0, 'Freq':{}})

    def print_rule_even_by_odd(self):
        """
        """
        di = {'e' + str(i) + 'xo' + str(j): len(self.even_odd['e' + str(i) + 'xo' + str(j)]) for i in range(0, self.doz_by_raffle + 1) for j in reversed(range(0, self.doz_by_raffle + 1))  if (i+j) == self.doz_by_raffle}
        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    ##### Methods for Printing #####
    def print_more_often_unit (self):
        """
        """
        di = {'x' + str(i): len(self.unit['x' + str(i)]) for i in range(0, 10)}

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        for each in sorted_list:
            print(each)

    def prepare_to_print(self, key):
        """
        """
        di ={} 
        for ind, val in enumerate(self.all_stat):
            num = ind + 1
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)
            di[str(el)] = val[key]

        sorted_list = sorted(di.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_list)

    def print_freq_dict(self):
        """
        """
        for ind, each in enumerate(self.all_stat):
            dic = each['Freq']
            sorted_list = sorted(dic.items(), key=operator.itemgetter(0), reverse=False)
            print(str(ind))
            print(str(sorted_list))

    def print_full_data(self):
        """
        """
        for el in self.all_content:
            print(el)
        #    for k, v in el.items():
        #        print(k + ':' + repr(v))


    ##### Methods for Plotting #####
    def plot_rule (self):
        """
        """
        done = False

        while not done :
            dic = {str(i + 1): 'e' + str(i) + 'xo' + str(j) for i in range(0, self.doz_by_raffle + 1) for j in reversed(range(0, self.doz_by_raffle + 1))  if (i+j) == self.doz_by_raffle}
            cmd = utils.print_second_menu()

            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.even_odd):
                    vals.append(len(self.even_odd[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.even_odd.items():
                    dic[k] = len(v)
                sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
                for each in sorted_list:
                    (k, v) = each
                    vals.append(v)
                    keys.append(k)

                plt.plot(vals)
                plt.xticks(np.arange(len(keys)), keys)
                plt.show()

            elif cmd == 'bar' :
                for i, k in enumerate(self.even_odd):
                    plt.bar(i, len(self.even_odd[k]))

                plt.xticks(np.arange(len(self.even_odd)) + 0.4, self.even_odd.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False

                while not done :

                    print ('')
                    print ('\033[92m' + "Choose the rule option:" + '\033[0m')
                    print ('')
                    for el in range(0, self.doz_by_raffle + 1):
                        print ("{} - {}".format(el + 1, 'e' + str(el) + 'xo' + str(self.doz_by_raffle - el)))
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter your option (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.even_odd[dic[cmd]]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label=dic[cmd])
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'freq' :
                done = False

                while not done :

                    print ('')
                    print ('\033[92m' + "Choose the rule option:" + '\033[0m')
                    print ('')
                    for el in range(0, self.doz_by_raffle + 1):
                        print ("{} - {}".format(el + 1, 'e' + str(el) + 'xo' + str(self.doz_by_raffle - el)))
                    print ("done  : exit the program")
                    print ('')
                    cmd = raw_input('\033[92m' + 'Enter your option (or done): ' + '\033[0m')
                    print ('')

                    if cmd == 'done' :
                        break

                    delay = []
                    v = self.even_odd[dic[cmd]]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label=dic[cmd])
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    def plot_unit (self):
        """
        """
        done = False

        while not done :

            print ('')
            print ('\033[92m' + "The following commands are available: " + '\033[0m')
            print ('')
            print ("pie   : show the data plotted on a pie chart")
            print ("bar   : show the data plotted on a bar chart")
            print ("line  : show the data plotted on a line chart")
            print ("delay : show the delay over the raffles, plus the average delay")
            print ("freq  : show the frequency of delays")
            print ("done  : exit the program")
            print ('')
            cmd = raw_input('\033[92m' + 'Enter a command: ' + '\033[0m')
            print ('')

            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.unit):
                    vals.append(len(self.unit[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.unit.items():
                    dic[k] = len(v)
                sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
                for each in sorted_list:
                    (k, v) = each
                    vals.append(v)
                    keys.append(k)

                plt.plot(vals)
                plt.xticks(np.arange(len(keys)), keys)
                plt.show()

            elif cmd == 'bar' :
                for i, k in enumerate(self.unit):
                    plt.bar(i, len(self.unit[k]))

                plt.xticks(np.arange(len(self.unit)) + 0.4, self.unit.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False

                while not done :
                    opt = utils.print_option_menu(9)

                    if opt == 'done' :
                        break

                    delay = []
                    v = self.unit['x' + opt]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label='x' + opt)
                    print (delay)
                    plt.show()

            elif cmd == 'freq' :
                done = False

                while not done :
                    opt = utils.print_option_menu(9)

                    if opt == 'done' :
                        break

                    delay = []
                    v = self.unit['x' + opt]
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label='x' + opt)
                    print (delay)
                    plt.show()

            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    def plot_more_often(self):
        """
        """
        num = int(raw_input('\033[92m' + 'Enter a number to plot (or 0 for none): ' + '\033[0m'))
        if num == 0:
            return

        aver = []
        for ind in range(len(self.all_stat[num - 1]['Occur']) - 1):
            aver.append(self.all_stat[num - 1]['Average'])

        plt.hist(self.all_stat[num - 1]['Delay'], len(self.all_stat[num - 1]['Delay']))
        #plt.plot(aver, label='Average') 
        plt.show()

    def plot_doze (self):
        """
        """
        done = False

        while not done :
            cmd = utils.print_second_menu()

            if cmd == 'pie' :
                #Pie chart
                vals = []
                keys = []
                for i, k in enumerate(self.doze):
                    vals.append(len(self.doze[k]))
                    keys.append(k)

                plt.figure(figsize=(6,6))
                plt.pie(vals, labels=keys, autopct='%1.1f%%')
                plt.show()

            elif cmd == 'line' :
                vals = []
                keys = []
                dic = {}
                for k, v in self.doze.items():
                    dic[k] = len(v)
                sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
                for each in sorted_list:
                    (k, v) = each
                    vals.append(v)
                    keys.append(k)

                plt.plot(vals)
                plt.xticks(np.arange(len(keys)), keys)
                plt.show()

            elif cmd == 'bar' :
                for i, k in enumerate(self.doze):
                    plt.bar(i, len(self.doze[k]))

                plt.xticks(np.arange(len(self.doze)) + 0.4, self.doze.keys())
                plt.show()

            elif cmd == 'delay' :
                done = False

                while not done :
                    opt = utils.print_option_menu(self.dozen_dozens)

                    if opt == 'done' :
                        break

                    delay = []
                    v = self.doze[opt + 'x']
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    plt.plot(delay, label=opt + 'x')
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'freq' :
                done = False

                while not done :
                    opt = utils.print_option_menu(self.done)

                    if opt == 'done' :
                        break

                    delay = []
                    v = self.doze[opt + 'x']
                    for ind in range(len(v) - 1):
                        delay.append(v[ind + 1] - v[ind])
                    delay.sort()
                    plt.plot(delay, label=opt + 'x')
                    print (delay)
                    plt.title('Delay')
                    plt.xlabel('Times raffled')
                    plt.ylabel('Delay between raffles')
                    plt.legend()
                    plt.show()

            elif cmd == 'done' :
                done = True
            else :
                print ("I don't understand the command " + cmd)

    ##### Methods for Computing #####
    def build_occur_list(self):
        """
        """
        for each in self.all_content:
            for el in each['Dozens']:
                self.all_stat[int(el) - 1]['Occur'].append(int(each['Number']))

    def build_delay_list(self):
        """
        """
        for each in self.all_stat:
            value = each['Occur']
            for ind in range(len(value) - 1):
                each['Delay'].append(value[ind + 1] - value[ind])

    def build_freq_dict(self):
        """
        """
        for each in self.all_stat:
            for el in set(each['Delay']):
                each['Freq'][str(el)] = each['Delay'].count(el)


    def fill_up_stand_dev(self):
        """
        """
        for each in self.all_stat:
            each['Std_Dev'] = utils.standard_deviation(each['Delay'], each['Average'])

    def fill_up_stand_sco(self):
        """
        """
        for each in self.all_stat:
            each['Std_Sco'] = abs(utils.standard_score(each['Last'], each['Average'], each['Std_Dev']))

    def more_often_num(self):
        """
        """
        for ind, val in enumerate(self.all_stat):
            val['More'] = len(val['Occur'])

    def last_time(self):
        """
        """
        for ind, val in enumerate(self.all_stat):
            val['Last'] = int(self.all_content[-1]['Number']) - val['Occur'][-1]

    def most_delay(self):
        """
        """
        for el in self.all_stat:
            el['Worst'] = max(el['Delay'])

    def aver_delay(self):
        """
        """
        for el in self.all_stat:
            el['Average'] = int(utils.mean(el['Delay']))

    def more_often_unit (self):
        """
        """
        for each in self.all_content:
            for el in each['Dozens']:
                u = utils.ret_unit(int(el))
                self.unit['x' + str(u)].append(int(each['Number']))

    def suggest_num(self, method='Score', for_print=True):
        """
        """

        result = {}
        st = 'x'
        for ind, val in enumerate(self.all_stat):
            num = ind + 1
            if num < 10:
                el = '0' + str(num)
            else:
                el = str(num)

            if method == 'Most Recently':
                result[el] = val['More']/100 - val['Last']/10 #
            elif method == 'Least Recently':
                result[el] = val['More']/100 + val['Last']/10 #
            elif method == 'Score':
                result[el] = val['More']/100 - val['Std_Sco']*2 #

            try:
                result[el] += val['Freq'][str(val['Last'])]
            except KeyError:
                result[el] += 0

            doz = utils.dozen(num)
            result[el] += len(self.doze[str(doz)+st])/1000 #Weight 1/10

            uni = utils.ret_unit(num)
            result[el] += len(self.unit[st+str(uni)])/1000 #Weight 1/10

            sorted_list = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        if for_print:
            print('##################### MORE OFTEN #####################')
            self.prepare_to_print('More')
            print('################## MORE OFTEN DOZENS #####################')
            self.print_more_often_dozen()
            print('################## MORE OFTEN UNITS #####################')
            self.print_more_often_unit()
            print('################# SUGGESTED NUMBERS #####################')
            print(sorted_list)
        else:
            return sorted_list

    def look_up_num(self):
        """
        """
        print ('Enter with ' + str(self.doz_by_raffle) + ' numbers:')
        dozens = []
        for el in range(self.doz_by_raffle):
            num = raw_input('Dozen number ' + str(el + 1) + ':')
            if int(num) < 10 and len(num) < 2:
                num = '0' + str(num)
            else:
                num = str(num)
            dozens.append(num)
        dozens.sort()

        founded = False
        for each in self.all_content:
            if dozens == each["Dozens"]:
                founded = True
                print ('')
                print ('\033[92m' + 'Dozens founded :' + '\033[0m')
                print ('Date : ' + each['Date'])

        if not founded:
            # TODO: Test the numbers with/against the statistics
            print ('Dozens not founded')

    def more_often_dozen (self):
        """
        """
        for each in self.all_content:
            d = 0
            for el in each['Dozens']:
                d = utils.dozen(int(el))
                self.doze[str(d) + 'x'].append(int(each['Number']))

    def rule_even_by_odd(self):
        """
        """
        for each in self.all_content:
            even = 0
            odd = 0
            for el in each["Dozens"]:
                if utils.isodd(int(el)):
                    odd += 1
                else:
                    even += 1

            self.even_odd['e' + str(even) + 'xo' + str(odd)].append(int(each['Number']))

    def screen_interf (self):
        """
        """
        done = False

        while not done :
            cmd = utils.print_main_menu ()

            if cmd == 'more' :
                self.prepare_to_print('More')
                self.plot_more_often()

            elif cmd == 'last' :
                self.prepare_to_print('Last')

            elif cmd == 'aver' :
                self.prepare_to_print('Average')

            elif cmd == 'wors' :
                self.prepare_to_print('Worst')

            elif cmd == 'show' :
                self.print_full_data()

            elif cmd == 'rule' :
                self.print_rule_even_by_odd()
                self.plot_rule()

            elif cmd == 'doze' :
                self.print_more_often_dozen()
                self.plot_doze()

            elif cmd == 'unit' :
                self.print_more_often_unit()
                self.plot_unit()

            elif cmd == 'look' :
                self.look_up_num()

            elif cmd == 'sugm' :
                self.suggest_num(method='Most Recently')

            elif cmd == 'sugl' :
                self.suggest_num(method='Least Recently')

            elif cmd == 'sugs' :
                self.suggest_num(method='Score')

            elif cmd == 'occu' :
                self.prepare_to_print('Occur')

            elif cmd == 'dela' :
                self.prepare_to_print('Delay')

            elif cmd == 'devi' :
                self.prepare_to_print('Std_Dev')

            elif cmd == 'scor' :
                self.prepare_to_print('Std_Sco')

            elif cmd == 'freq':
                self.print_freq_dict()

            elif cmd == 'done' :
                done = True

            elif cmd == 'test' :
                print('#### MORE ####')
                self.prepare_to_print('More')
                print('#### LAST ####')
                self.prepare_to_print('Last')
                print('#### DELAY AVERAGE####')
                self.prepare_to_print('Average')
                print('#### WORST DELAY ####')
                self.prepare_to_print('Worst')
                print('#### RULE 3 by 2 ####')
                self.print_rule_even_by_odd()
                print('#### DOZE ####')
                self.print_more_often_dozen()
                print('#### UNIT ####')
                self.print_more_often_unit()
                self.suggest_num()
                self.suggest_num(method='Most Recently')
                self.suggest_num(method='Least Recently')
                self.prepare_to_print('Occur')
                self.prepare_to_print('Delay')
                self.prepare_to_print('Std_Dev')
                self.prepare_to_print('Std_Sco')

            else :
                print ("I don't understand the command " + cmd)

if __name__ == '__main__':
    print('lottery.py')
