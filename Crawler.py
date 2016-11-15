from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
# these are libraries for the good and bad words
positive = []
negative = []
sent = []

# opening all of the libraries and putting each word into their following lists
fo = open('positive.txt', 'r')
for line in fo:
    positive.append(line.replace('\n', ""))
fo.close()

fo = open('negative.txt', 'r')
for line in fo:
    negative.append(line.replace('\n', ""))
fo.close()

fo = open('sent_words.txt', 'r')
for line in fo:
    sent.append(line.replace('\n', "").split('\t'))
fo.close()

# this is the crawler

final_list = []
# The tid is the teacher id so we are starting with 10000 randomly picked id number
tid = 10000
number_teachers = 5
number_teachers = 5 + tid
# this while loop runs as long as you define it to
while tid != number_teachers:
    # print tid to keep track
    print(tid)
    url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(tid)
    # gets the source code/HTML for the url
    source_code = requests.get(url)
    # this pushes the code through the beautiful soup parser
    soup = BeautifulSoup(source_code.text, 'html.parser')

    html_rating = []
    html_comment = []

    # this goes to the td tag with class rating then div tag with class descriptor-container then to span class score
    for x in soup.find_all('td', {'class': 'rating'}):
        for y in x.find_all('div', {'class': 'descriptor-container'}):
            for a in (y.find_all('span', {'class', 'score'})):
                html_rating.append(a.string)

    # this goes to the td tag comments and finds all the p tags which are the comments
    for x in soup.find_all('td', {'class': 'comments'}):
        html_comment.append(x.p.string)

    # this is the senti word analysis

    # we set j = 0 to have a starting point for the inner if statement because the way things are loaded into array
    j = 0
    for i in range(len(html_rating)):
        # this is for the if statement mentioned above. It allows for 2 numbers to from html_rating to be
        # looked at followed by 1 from html_comment
        if i % 2 == 1:
            rating = 0.0
            # this is how we are storing results overall quality, level of difficulties,our rating, comment
            # checks if any words in positive word list are in html_comment if they are then it adds .5 to rating
            for x in positive:
                if x in html_comment[j].lstrip().lower():
                    rating += .5
            # checks if any words in positive word list are in html_comment if they are then it minuses .5 to rating
            for x in negative:
                if x in html_comment[j].lstrip().lower():
                    rating -= .5
            # checks if any words in positive word list are in html_comment if they are then it
            # adds certain value to the to rating
            for x in sent:
                if x[0] in html_comment[j].lstrip().lower():
                    rating += float(x[1])
            # the final list is made using dictionary to keep track and organize the data
            final_list.append({
                "Overall Rating": html_rating[i - 1],
                "Difficulty Rating": html_rating[i],
                "Senti Rating": rating,
                "Comment": html_comment[j].lstrip()
            })
            rating = 0.0
            j += 1
    tid += 1

# this is to make a graph

plot_Senti_Rating = []
plot_Overall_Rating = []
plot_Difficulty_Rating = []

# goes through the list and gives each rating to its appropriate field
for x in final_list:
    if float(x['Overall Rating']) >=0:
        plot_Senti_Rating.append(x['Senti Rating'])
        plot_Difficulty_Rating.append(float(x['Difficulty Rating']))
        plot_Overall_Rating.append(float(x['Overall Rating']))
        print('Overall Rating \t','Difficulty Rating \t', 'Senti Rating \n')
        print(x['Overall Rating'], '\t', x['Difficulty Rating'], '\t', x['Senti Rating'], '\n', x['Comment'], )


fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

ax1.set_xlabel('Overall Rating')
ax1.set_ylabel('Difficulty Rating')
ax1.set_zlabel('Senti Rating')

ax1.scatter(plot_Overall_Rating, plot_Difficulty_Rating, plot_Senti_Rating)
plt.show()

