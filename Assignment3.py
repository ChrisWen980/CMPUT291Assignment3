'''
CMPUT 291 Winter 2021
Assignment 3
Ahmad Amin, Chris Wen
'''

'''
To Do:

Clarify with TA:
For p1, p2 do we need different erorr message for valid area/email with no output vs invalid area/email?
For p1, p2 do we lose marks for "for name in rows: print name[0]" (is there a way to do this in SQL?)

Implement error handling in option 4
Implement option 4
"Some simple error handling should be performed, and the application should not crash "easily.”
For instance, in Task #1 (#2) if one provides an area (user email) that does not exist, instead of returning an empty result, an error message should indicate the issue.
Likewise in Tasks #3 and #4 the application should enforce that X and Y are positive numbers."
'''
import sqlite3

def dbOption(Option):
    '''
    This function contains the implementation for the four options.
    '''
    
    if (Option == 1):
        print("You chose Option 1: Find accepted papers.")

        # Implement Query 1 here:
        # List the titles of accepted papers in a given area, that have at least one review and where area is to be provided at query time, in descending
        # order of their average overall review scores. 

        print("Please choose an area: ", end = '')
        Area = input()
        Decision = 'A'
        
        c.execute("SELECT DISTINCT(papers.title) FROM papers JOIN reviews ON papers.id = reviews.paper WHERE papers.area=:area AND papers.decision=:decision GROUP BY papers.id HAVING COUNT(reviews.reviewer) >= 1 ORDER BY avg(reviews.overall) DESC;",
        {"area":Area, "decision":Decision})
        rows=c.fetchall()
        if not rows:
            print("No accepted paper titles given this area")
        else:
            for name in rows:
                print(name[0])

    elif (Option == 2):
        print("You chose Option 2: Find papers assigned for review.")

        # Implement Query 2 here:
        # Given a user's email, which is to be provided at query time, list only the titles of the papers he/she was assigned to review. The papers should 
        # be ordered by their (paper) ids (even though that is not to be displayed).  If users were not assigned to review any paper, an informative answer, 
        # e.g, "No paper has been assigned to this reviewer” should be displayed.

        print("Please choose an email: ", end = '')
        Email = input()
        c.execute("SELECT p.title FROM papers p, reviews r WHERE r.paper = p.id AND r.reviewer=:email ORDER BY p.id", {"email":Email})
        rows=c.fetchall()
        if not rows:
            print("No paper has been assigned to this reviewer")
        else:
            for name in rows:
                print(name[0])

    elif (Option == 3): 
        print("You chose Option 3: Find papers with inconsistent reviews.")
        inputCorrect = True

        # Implement Query 3 here:
        # A review for a paper is inconsistent wrt others if it has an overall mark different by more than X% (above of below) of the average of all 
        # "overall mark” for that paper. List the id and title of every paper with at least one inconsistent reviews, where X is to be provided at query time.

        print("Please enter a percentage [X]% to find papers inconsistent reviews: ", end = '')
        try:
            Percentage = float(input()) * 0.01
        except:
            print("Error: Percentage is of wrong type")
            inputCorrect = False
        
        if inputCorrect and Percentage < 0:
            print("Error: Percentage must be positive")
            inputCorrect = False
            
        if inputCorrect:
            c.execute("SELECT DISTINCT p.title, p.id FROM papers p, reviews r WHERE r.paper = p.id AND :percent < ABS(1 - r.overall / (SELECT avg(r2.overall) FROM reviews r2 WHERE r2.paper = p.id));",
            {'percent': Percentage})
            rows=c.fetchall()
            if not rows:
                print("No inconsistent reviews with given percentage")
            else:
                for name, iid in rows:
                    print(f"{iid} {name}")

    elif (Option == 4):
        print("You chose Option 4: Find papers according to difference score.")
        inputCorrect = True
        # Implement Query 4 here:
        # Create a VIEW called (exactly) "DiffScore” which contains three columns: "pid” (the paper's id), "ptitle” (the paper's title) and "difference” 
        # (for each paper how much its average score is different, in absolute value, from the average score of all papers in the same area). Using DiffScore
        #  --which is to be created only once when the application is opened-- find the email addresses and names of the reviewers that have reviewed a paper 
        # with a "difference” between X (inclusive) and Y (inclusive) where X and Y are to be provided at query time.
        #c.execute("SELECT * FROM DiffScore;")

        print("Please enter a range from [X] to [Y].")
        print("X: ", end = "")
        try:
            X = float(input())
        except:
            print("Error: range is of wrong type")
            inputCorrect = False

        if inputCorrect and X < 0:
            print("Error: range boundary negative")
            inputCorrect = False
        
        if inputCorrect:
            print("Y: ", end = "")
            try:
                Y = float(input())
            except:
                print("Error: range is of wrong type")
                inputCorrect = False

        if inputCorrect and Y < 0:
            print("Error: range boundary negative")
            inputCorrect = False

        if inputCorrect:
            c.execute("SELECT u.email, u.name FROM reviews r, users u, DiffScore d WHERE ((d.difference <= :x AND d.difference >= :y) OR (d.difference >= :x AND d.difference <= :y)) AND d.pid = r.paper AND r.reviewer = u.email",
            {'x': X, 'y': Y})
            rows=c.fetchall()
            if not rows:
                print("No reviewers given this range")
            else:
                for email, name in rows:
                    print(f"{email} {name}")

    else: #option = 5
        print("You chose Option 5: Exit.")

def getOption():
    '''
    This function gets input from user, if input is correct (inside the set {1,2,3,4,5}) then return input.
    Else returns 0.
    '''
    option = input()
    try:
        option = int(option)
    except:
        print("Error: Option choice is of incorrect type")
        return 0
    
    if option in {1, 2, 3, 4, 5}:
        return option
    
    print("Error: Option choice must be 1, 2, 3, 4, or 5")
    return 0
        
def interface():
    '''
    This function handles the interface portion.
    Calls getOption() to handle input.
    Calls dbOption() to process input.
    '''

    print("Welcome to the conference management system")

    Option = 0

    while(Option != 5):
        print("\n")
        print("Please select an option by entering a number: ")
        print("1. Find accepted papers")
        print("2. Find papers assigned for review")
        print("3. Find papers with inconsistent reviews")
        print("4. Find papers according to difference score")
        print("5. Exit")
        print("Option: ", end = '')
        
        temp = getOption()

        if temp:
            Option = temp
            dbOption(temp)
        
    print("Conference management system will now terminate")

if __name__ == "__main__":
    conn = sqlite3.connect('A3.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    conn.commit()
    c.execute("DROP VIEW IF EXISTS DiffScore;")
    c.execute("CREATE VIEW DiffScore AS SELECT DISTINCT p.id AS pid, p.title AS ptitle, ABS((SELECT avg(r3.overall) FROM reviews r3 WHERE r3.paper = p.id) - (SELECT avg(r2.overall) FROM reviews r2, papers p2 WHERE r2.paper = p2.id AND p2.area = p.area GROUP BY p2.area)) AS difference FROM papers p, reviews r WHERE r.paper = p.id;")
    interface()
    conn.close()
