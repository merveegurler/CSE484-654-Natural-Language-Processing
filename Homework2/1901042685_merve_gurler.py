# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 14:52:34 2021

@author: HP
"""

from nltk import ngrams
import os 
import random

total_word_num = 0
last_ind = 0

def choose_rand_gram(last_syllable,grams,probabilities,n):
    all_prob = {}
    second_choice = {}
    string = {}
    temp = ""
    j = 0
    k = 0
    count = 0

    for i in grams.split('\n'):
      i = i.replace(')', '')
      i = i.replace('(', ' ')
      string = i.split(',')
      if k < (grams.count('\n') - 1):
        second_choice = i
      if k < (grams.count('\n') - 1) and last_syllable == string[0] and n > 1:
        temp = ""
        for t in range(0, n):
          if t < n-1:
            temp += string[t] + ','
          else:
            temp += string[t]
        all_prob[j] = temp
        j += 1
      if n == 1:
        ind = find_max_probability(grams, probabilities,last_ind)
        for i in grams.split('\n'):
          i = i.replace(')', '')
          i = i.replace('(', ' ')
          string = i.split(',')
          if count < len(probabilities) and probabilities[count] == probabilities[ind]:
            all_prob[j] = string[0]
            j += 1
          count += 1
      k += 1
    if bool(all_prob):
      return random.choice(all_prob)
    else:
      return second_choice

def find_max_probability(grams, probabilities,last_ind):
    count = 0
    max_prob = 0
    max_prob_ind = 0

    for i in grams.split('\n'):
      if probabilities[count] > max_prob and count != last_ind:
          max_prob = probabilities[count]
          max_prob_ind = count
          last_ind = count
      count += 1     
    return max_prob_ind

def create_paragraphs(grams, probabilities, ind, name,n):
    count = 0
    string1 = {}
    string2 = ""

    f = open(name, 'w', encoding = "utf-8")
    for i in grams.split('\n'):
      if count < len(probabilities) and probabilities[count] == probabilities[ind]:
        f.write(i)
        i = i.replace(')', '')
        i = i.replace('(', ' ')
        string = i.split(',')
        if bool(string):
          string1[n-1] = string[n-1]
          for k in range(0,10):
            rand_gram = choose_rand_gram(string1[n- 1],grams,probabilities,n)
            rand_gram = rand_gram.replace(')', '')
            rand_gram = rand_gram.replace('(', ' ')
            string1 = rand_gram.split(',')
            string2 = ""
            if n > 1:
              for l in range(1, n):
                if l < n-1:
                  string2 += string1[l] + ' '
                else:
                  string2 += string1[l]
              f.write(str(string2))
            else:
              f.write(str(string1[0]))
          break
      count += 1
    f.close()


def calculate_perplexity_of_sentences(grams, probabilities, name,total_word_num):
    count = 0
    perplexity = 0
    flag = 0

    f = open(name, 'w', encoding = "utf-8")
    for i in grams.split('\n'):
        i = i.replace(')', '')
        i = i.replace('(', ' ')
        string = i.split(',')
        dot = ' \'.\''
        if string[0] == dot:
            if flag == 0:
              perplexity = probabilities[count]
            else:
              perplexity *= probabilities[count]
            f.write("%s %s %s" % (string[1], str(perplexity), '\n'))
            if perplexity != 0:
              perplexity = 1 / perplexity
              perplexity = perplexity**(1/total_word_num)
            else:
              print(calculate_probability_GT_smoothing(grams,total_word_num))
              perplexity = calculate_probability_GT_smoothing(grams,total_word_num)
              perplexity = 1 / perplexity
              perplexity = perplexity**(1/total_word_num)
            perplexity = 0
            flag = 0
            count += 1
        else:
            f.write(string[0] + '')
            if flag == 0:
              perplexity = probabilities[count]
            else:
              perplexity *= probabilities[count]
            flag = 1
            count += 1
    return perplexity


def calculate_probability_GT_smoothing(grams,total_word_num):
    occured_ones = 0
    grams = grams.replace(')', '')
    grams = grams.replace('(', ' ')

    for i in grams.split('\n'):
        i = i.replace(')', '')
        i = i.replace('(', ' ')
        string = i.split(',')
        if (grams.count(string[0]) == 1):
             occured_ones += 1
    if occured_ones > 0:
      probability = occured_ones / total_word_num
    else:
      probability = 1 / total_word_num
    print(str(probability))
    return probability


def calculate_probabilities(gram, grams,total_word_num,n):
    probability = 0
    
    for i in range(0, gram.count(',')):
        gram = gram.replace(')', '')
        gram = gram.replace('(', ' ')
        grams = grams.replace(')', '')
        grams = grams.replace('(', ' ')
        string = gram.split(',')
        for j in range(0, n-1):
          if n > 1:
            pay = string[j] + ',' + string[j+1]
            if grams.count(string[j+1]) != 0 and grams.count(pay) != 0:
                if i == 0:
                    probability = (grams.count(pay) / grams.count(string[j+1]))
                else:
                    probability = (grams.count(pay) / grams.count(string[j+1])) * probability
            else:
                if i == 0:
                    probability = calculate_probability_GT_smoothing(grams,total_word_num)
                else:
                    probability *= calculate_probability_GT_smoothing(grams,total_word_num)
          else:
            pay = string[j]
            if grams.count(string[j]) != 0 and grams.count(pay) != 0:
                if i == 0:
                    probability = (grams.count(pay) / grams.count(string[j]))
                else:
                    probability = (grams.count(pay) / grams.count(string[j])) * probability
            else:
                if i == 0:
                    probability = calculate_probability_GT_smoothing(grams,total_word_num)
                else:
                    probability *= calculate_probability_GT_smoothing(grams,total_word_num)
    return probability



################ To create N-gram Tables ###############

######################## calculating 1-Grams #########################

with open('train.txt', encoding='utf-8') as f:
    lines = f.read()

f = open("1gram.txt", 'w', encoding = "utf-8")

n = 1
bigrams = ngrams(lines.split(), n)

for grams in bigrams:
    f.write(grams.__str__() + '\n')
    
with open('1gram.txt', encoding='utf-8') as f:
    grams = f.read()

total_word_num = grams.count('\n') + 1

f = open("1gram_prob_train.txt", 'w', encoding = "utf-8")

j = 0
probability_ar = {}

for i in grams.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar[j] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    j += 1
    
calculate_perplexity_of_sentences(grams, probability_ar, "1gram_perplexities_train.txt",total_word_num)
    
################ To test model ################
    
with open('test.txt', encoding='utf-8') as f:
    test = f.read()

n = 1
bigrams_test = ngrams(test.split(), n)

f = open("1gram_test.txt", 'w', encoding = "utf-8")

for grams in bigrams_test:
    f.write(grams.__str__() + '\n')
    
with open('1gram_test.txt', encoding='utf-8') as f:
    grams_test = f.read()
    
with open('1gram.txt', encoding='utf-8') as f:
    grams = f.read()

f = open("1gram_prob_test.txt", 'w', encoding = "utf-8")

k=0
probability_ar_2 = {}

for i in grams_test.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar_2[k] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    k += 1

calculate_perplexity_of_sentences(grams_test, probability_ar_2, "1gram_perplexities_test.txt",total_word_num)

ind = 0
ind = find_max_probability(grams, probability_ar,last_ind)

create_paragraphs(grams, probability_ar, ind, "1gram_paragraphs.txt",n)

######################## calculating 2-Grams #########################
with open('train.txt', encoding='utf-8') as f:
    lines = f.read()

f = open("2gram.txt", 'w', encoding = "utf-8")

n = 2
bigrams = ngrams(lines.split(), n)

for grams in bigrams:
    f.write(grams.__str__() + '\n')
    
with open('2gram.txt', encoding='utf-8') as f:
    grams = f.read()

total_word_num = grams.count('\n') + 1

f = open("2gram_prob_train.txt", 'w', encoding = "utf-8")

j = 0
probability_ar = {}

for i in grams.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar[j] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    j += 1
    
calculate_perplexity_of_sentences(grams, probability_ar, "2gram_perplexities_train.txt",total_word_num)
    
################ To test model ################
    
with open('test.txt', encoding='utf-8') as f:
    test = f.read()

n = 2
bigrams_test = ngrams(test.split(), n)

f = open("2gram_test.txt", 'w', encoding = "utf-8")

for grams in bigrams_test:
    f.write(grams.__str__() + '\n')
    
with open('2gram_test.txt', encoding='utf-8') as f:
    grams_test = f.read()
    
with open('2gram.txt', encoding='utf-8') as f:
    grams = f.read()

f = open("2gram_prob_test.txt", 'w', encoding = "utf-8")

k=0
probability_ar_2 = {}

for i in grams_test.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar_2[k] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    k += 1

calculate_perplexity_of_sentences(grams_test, probability_ar_2, "2gram_perplexities_test.txt",total_word_num)

ind = 0
ind = find_max_probability(grams, probability_ar,last_ind)

create_paragraphs(grams, probability_ar, ind, "2gram_paragraphs.txt",n)

######################## calculating 3-Grams #########################
with open('train.txt', encoding='utf-8') as f:
    lines = f.read()

f = open("3gram.txt", 'w', encoding = "utf-8")

n = 3
bigrams = ngrams(lines.split(), n)

for grams in bigrams:
    f.write(grams.__str__() + '\n')
    
with open('3gram.txt', encoding='utf-8') as f:
    grams = f.read()

total_word_num = grams.count('\n') + 1

f = open("3gram_prob_train.txt", 'w', encoding = "utf-8")

j = 0
probability_ar = {}

for i in grams.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar[j] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    j += 1
    
calculate_perplexity_of_sentences(grams, probability_ar, "3gram_perplexities_train.txt",total_word_num)
    
################ To test model ################
    
with open('test.txt', encoding='utf-8') as f:
    test = f.read()

n = 3
bigrams_test = ngrams(test.split(), n)

f = open("3gram_test.txt", 'w', encoding = "utf-8")

for grams in bigrams_test:
    f.write(grams.__str__() + '\n')
    
with open('3gram_test.txt', encoding='utf-8') as f:
    grams_test = f.read()
    
with open('3gram.txt', encoding='utf-8') as f:
    grams = f.read()

f = open("3gram_prob_test.txt", 'w', encoding = "utf-8")

k=0
probability_ar_2 = {}

for i in grams_test.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar_2[k] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    k += 1

calculate_perplexity_of_sentences(grams_test, probability_ar_2, "3gram_perplexities_test.txt",total_word_num)

ind = 0
ind = find_max_probability(grams, probability_ar,last_ind)

create_paragraphs(grams, probability_ar, ind, "3gram_paragraphs.txt",n)

######################## calculating 4-Grams #########################
with open('train.txt', encoding='utf-8') as f:
    lines = f.read()

f = open("4gram.txt", 'w', encoding = "utf-8")

n = 4
bigrams = ngrams(lines.split(), n)

for grams in bigrams:
    f.write(grams.__str__() + '\n')
    
with open('4gram.txt', encoding='utf-8') as f:
    grams = f.read()

total_word_num = grams.count('\n') + 1

f = open("4gram_prob_train.txt", 'w', encoding = "utf-8")

j = 0
probability_ar = {}

for i in grams.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar[j] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    j += 1
    
calculate_perplexity_of_sentences(grams, probability_ar, "4gram_perplexities_train.txt",total_word_num)
    
################ To test model ################
    
with open('test.txt', encoding='utf-8') as f:
    test = f.read()

n = 4
bigrams_test = ngrams(test.split(), n)

f = open("4gram_test.txt", 'w', encoding = "utf-8")

for grams in bigrams_test:
    f.write(grams.__str__() + '\n')
    
with open('4gram_test.txt', encoding='utf-8') as f:
    grams_test = f.read()
    
with open('4gram.txt', encoding='utf-8') as f:
    grams = f.read()

f = open("4gram_prob_test.txt", 'w', encoding = "utf-8")

k=0
probability_ar_2 = {}

for i in grams_test.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar_2[k] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    k += 1

calculate_perplexity_of_sentences(grams_test, probability_ar_2, "4gram_perplexities_test.txt",total_word_num)

ind = 0
ind = find_max_probability(grams, probability_ar,last_ind)

create_paragraphs(grams, probability_ar, ind, "4gram_paragraphs.txt",n)

######################## calculating 5-Grams #########################
with open('train.txt', encoding='utf-8') as f:
    lines = f.read()

f = open("5gram.txt", 'w', encoding = "utf-8")

n = 5
bigrams = ngrams(lines.split(), n)

for grams in bigrams:
    f.write(grams.__str__() + '\n')
    
with open('5gram.txt', encoding='utf-8') as f:
    grams = f.read()

total_word_num = grams.count('\n') + 1

f = open("5gram_prob_train.txt", 'w', encoding = "utf-8")

j = 0
probability_ar = {}

for i in grams.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar[j] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    j += 1
    
calculate_perplexity_of_sentences(grams, probability_ar, "5gram_perplexities_train.txt",total_word_num)
    
################ To test model ################
    
with open('test.txt', encoding='utf-8') as f:
    test = f.read()

n = 5
bigrams_test = ngrams(test.split(), n)

f = open("5gram_test.txt", 'w', encoding = "utf-8")

for grams in bigrams_test:
    f.write(grams.__str__() + '\n')
    
with open('5gram_test.txt', encoding='utf-8') as f:
    grams_test = f.read()
    
with open('5gram.txt', encoding='utf-8') as f:
    grams = f.read()

f = open("5gram_prob_test.txt", 'w', encoding = "utf-8")

k=0
probability_ar_2 = {}

for i in grams_test.split('\n'):
    prob = calculate_probabilities(i, grams,total_word_num,n)
    probability_ar_2[k] = prob
    f.write("gram: %s\tProbability: %lf\n" % (i, prob))
    k += 1

calculate_perplexity_of_sentences(grams_test, probability_ar_2, "5gram_perplexities_test.txt",total_word_num)

ind = 0
ind = find_max_probability(grams, probability_ar,last_ind)

create_paragraphs(grams, probability_ar, ind, "5gram_paragraphs.txt",n)

os.remove("1gram_test.txt")
os.remove("1gram.txt")

os.remove("2gram_test.txt")
os.remove("2gram.txt")

os.remove("3gram_test.txt")
os.remove("3gram.txt")

os.remove("4gram_test.txt")
os.remove("4gram.txt")

os.remove("5gram_test.txt")
os.remove("5gram.txt")