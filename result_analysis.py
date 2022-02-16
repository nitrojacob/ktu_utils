#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 18:58:20 2021

@author: jacob

Does result analysis of APJA-KTU results.
Download result xls for a semester from
KTU-Login(app.ktu.edu.in) > Results > Semester Grade Card Report > ... > Export as XLS

Provide the xls file as argument to this script.

"""

import pandas as pd
import argparse

class KTU2019Result(object):
    def __init__(self, xls, scheme=2019):
        self.df = pd.read_excel(args.xls, header=1)
        if scheme == '2015':
        	self.fail_tags = ['F', 'FE', 'I', 'AB', 'W/D']
        	self.pass_tags = ['O', 'A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'P']
        else: #2019 Scheme
        	self.fail_tags = ['F', 'FA', 'FS', 'I', 'AB', 'W/D']
        	self.pass_tags = ['S', 'A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'P']
        self.ofmt="{0:<10}{1:>10}{2:>10}{3:>10}"
        self.fail_count = {} #Subject wise fail counts
        self.pass_count = {} #Subject wise pass counts
        self.cols = self.df.columns
        self.allpass_count = 0
        self.student_count = self.df.shape[0]
    def analyse_pass_fail(self):
        for student in range(self.student_count):
            allpass = 1
            unknown_tags = []
            for col in self.cols[2:]:
                tag = self.df[col][student]
                if pd.isna(tag) or (not type(tag) == str):
                    continue
                if not col in self.fail_count.keys():
                    self.fail_count[col] = 0
                    self.pass_count[col] = 0
                if tag in self.fail_tags:
                    allpass = 0
                    self.fail_count[col] += 1
                elif tag in self.pass_tags:
                    self.pass_count[col] += 1
                elif tag not in self.pass_tags:
                    unknown_tags.append(tag)
            if allpass == 1:
                self.allpass_count += 1
            if len(unknown_tags) > 0:
                print('Following unknown tags encountered:', unknown_tags)
    def print_pass_fail(self, codes):
        print("Total Students:", self.student_count)
        print("All pass:" , self.allpass_count)
        print(self.ofmt.format("Code","#fail", "#pass", "%pass"))
        for subject in self.fail_count.keys():
            if codes != None:
                if subject in codes.split(','):
                    print(self.ofmt.format(subject, self.fail_count[subject], self.pass_count[subject], round((self.pass_count[subject]/(self.pass_count[subject] + self.fail_count[subject]))*100)))
            else:
                print(self.ofmt.format(subject, self.fail_count[subject], self.pass_count[subject], round((self.pass_count[subject]/(self.pass_count[subject] + self.fail_count[subject]))*100)))    
    def analyse_sgpa_cgpa(self):
        self.sgpa = pd.DataFrame(data = self.df.loc[:,'Student'], columns =['Student','Score'])
        self.sgpa['Score'] = self.df.loc[:,'SGPA']
        self.sgpa.sort_values('Score',ascending=False, inplace=True, ignore_index=True)
        self.cgpa = pd.DataFrame(data = self.df.loc[:,'Student'], columns =['Student','Score'])
        self.cgpa['Score'] = self.df.loc[:,'CGPA']
        self.cgpa.sort_values('Score',ascending=False, inplace=True, ignore_index=True)
    def print_sgpa_cgpa(self):
        sfmt='{0:<30}{1:>10}'
        
        print()
        print('SGPA toppers')
        print(sfmt.format('Name', 'SGPA'))
        for i in range(5):
            ktuid,name = self.sgpa.loc[i,'Student'].split('-')
            print(sfmt.format(name, self.sgpa.loc[i,'Score']))
        
        print()
        print('CGPA toppers')
        print(sfmt.format('Name', 'CGPA'))
        for i in range(5):
            ktuid,name = self.cgpa.loc[i,'Student'].split('-')
            print(sfmt.format(name, self.cgpa.loc[i,'Score']))
            
        print()
        print('SGPA Analysis')
        print(sfmt.format('SGPA Range', '#students'))
        print(sfmt.format('SGPA==10', result.sgpa[result.sgpa.Score == 10].shape[0]))
        gpa_bucket = [10, 9, 8, 7, 6, 5, 4, 0]
        for i in range(len(gpa_bucket)-1):
            ub = gpa_bucket[i]    #upper bound
            lb = gpa_bucket[i+1] #lower bound
            print(sfmt.format('SGPA <'+ str(ub)+' & >=' + str(lb), result.sgpa[(result.sgpa.Score < ub) & (result.sgpa.Score >= lb)].shape[0]))
        
        print()
        print('CGPA Analysis')
        print(sfmt.format('CGPA Range', '#students'))
        print(sfmt.format('CGPA==10', result.cgpa[result.cgpa.Score == 10].shape[0]))
        gpa_bucket = [10, 9, 8, 7, 6, 5, 4, 0]
        for i in range(len(gpa_bucket)-1):
            ub = gpa_bucket[i]    #upper bound
            lb = gpa_bucket[i+1] #lower bound
            print(sfmt.format('CGPA <'+ str(ub)+' & >=' + str(lb), result.cgpa[(result.cgpa.Score < ub) & (result.cgpa.Score >= lb)].shape[0]))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Do result analysis on file obtained from KTU login")
    parser.add_argument("xls", help=".xls file containing grades; downloaded from KTU site")
    parser.add_argument("-c", "--codes", default=None, help="the comma separated list of subject codes you want at output. Omitting this argument will print only subjects where there are atleast 1 student have pass/fail grade")
    parser.add_argument("-s", "--scheme", default=2019, help="KTU batch scheme 2015/2019")
    args = parser.parse_args()

    result = KTU2019Result(args.xls, args.scheme)
    result.analyse_pass_fail()
    result.print_pass_fail(args.codes)
    result.analyse_sgpa_cgpa()
    result.print_sgpa_cgpa()
