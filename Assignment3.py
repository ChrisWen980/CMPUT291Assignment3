import sqlite3


# This function contains the 4 options
def dbOption(Option):
    if (Option == 1):
        # This statement can be removed later
        print("You chose Option 1: Find accepted papers.")

        # Implement Query 1 here:
        # List the titles of accepted papers in a given area, that have at least one review and where area is to be provided at query time, in descending
        # order of their average overall review scores. 

        print("Please choose an area: ", end = '')
        Area = str(input())
        Decision = 'A'
        
        c.execute("SELECT DISTINCT(papers.title), COUNT(reviews.reviewer) FROM papers JOIN reviews ON papers.id = reviews.paper WHERE papers.area=:area AND papers.decision=:decision GROUP BY papers.id HAVING COUNT(reviews.reviewer) >= 1 ORDER BY avg(reviews.overall) DESC;",
        {"area":Area, "decision":Decision})
        rows=c.fetchall()
        print(rows)


        #c.execute("PRAGMA table_info(reviews)")
        #print(c.fetchall())
        #c.execute("PRAGMA table_info(papers)")
        #print(c.fetchall())




    elif (Option == 2):
        # This statement can be removed later
        print("You chose Option 2: Find papers assigned for review.")

        # Implement Query 2 here:
        # Given a user's email, which is to be provided at query time, list only the titles of the papers he/she was assigned to review. The papers should 
        # be ordered by their (paper) ids (even though that is not to be displayed).  If users were not assigned to review any paper, an informative answer, 
        # e.g, "No paper has been assigned to this reviewer” should be displayed.



    elif (Option == 3): 
        # This statement can be removed later
        print("You chose Option 3: Find papers with inconsistent reviews.")

        # Implement Query 3 here:
        # A review for a paper is inconsistent wrt others if it has an overall mark different by more than X% (above of below) of the average of all 
        # "overall mark” for that paper. List the id and title of every paper with at least one inconsistent reviews, where X is to be provided at query time.

        print("Please enter a percentage [X]% to find papers inconsistent reviews: ", end = '')
        Percentage = float(input()) * 0.01
        
        c.execute("SELECT DISTINCT(papers.title), papers.id FROM papers JOIN reviews ON papers.id = reviews.paper GROUP BY reviews.paper HAVING (reviews.overall < (avg(reviews.overall) - (:percent * avg(reviews.overall))) OR reviews.overall > (avg(reviews.overall) + (:percent * avg(reviews.overall))));",
        {'percent': Percentage})
        rows=c.fetchall()
        print(rows)



    elif (Option == 4):
        # This statement can be removed later
        print("You chose Option 4: Find papers according to difference score.")

        # Implement Query 4 here:
        # Create a VIEW called (exactly) "DiffScore” which contains three columns: "pid” (the paper's id), "ptitle” (the paper's title) and "difference” 
        # (for each paper how much its average score is different, in absolute value, from the average score of all papers in the same area). Using DiffScore
        #  --which is to be created only once when the application is opened-- find the email addresses and names of the reviewers that have reviewed a paper 
        # with a "difference” between X (inclusive) and Y (inclusive) where X and Y are to be provided at query time.



    elif (Option == 5):
        print("You chose Option 5: Exit.")

    else:
        print("Invalid choice, please select another.")
        
        
        
        

# Welcome interface statement

print("Welcome to the conference management system")

Option = 0
conn = sqlite3.connect('A3.db')
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')
conn.commit()

inputType = False

while(Option != 5):
    # Interface Setup Statements
    print("\n")
    print("Please select an option by entering a number: ")
    print("1. Find accepted papers")
    print("2. Find papers assigned for review")
    print("3. Find papers with inconsistent reviews")
    print("4. Find papers according to difference score")
    print("5. Exit")
    print("Option: ", end = '')

    # User enters in a number which will represent a question
    
    try:
        Option = int(input())
        inputType = True
    except:
        print("Option choice is of incorrect type")

    if (inputType == True):
        dbOption(Option)
        inputType = False
    
print("Conference management system will now terminate")
conn.close()