# Importing the pandas module
import pandas as pd

# Loading in datasets/users.csv 
logins = pd.read_csv("datasets/logins.csv")

# Rule 1: Not too short
# Create a boolean variable
length_check = logins['password'].str.len() >= 10
# Separate using boolean indexing
valid_pws = logins[length_check]
bad_pws = logins[~length_check]

# Rule 2: All the types of characters
# Let's create a boolean index for each character requirement
# [ ] is used to indicate a set of characters
# e.g. [abc] will match 'a', 'b', or 'c'.
# We can use a-z to represent all lowercase chars between a and Z
lcase = valid_pws['password'].str.contains('[a-z]') 
ucase = valid_pws['password'].str.contains('[A-Z]')
special = valid_pws['password'].str.contains('\W')
# \d matches any decimal digit; this is equivalent to doing [0-9]
# \W matches any non-alphanumeric character
numeric = valid_pws['password'].str.contains('\d')
# A password needs to have all these as true 
# If any of these are false, we need it to return false
# In other words, all of these have to be true to return true
# We can use the & (and) operator
char_check = lcase & ucase & numeric & special
bad_pws = bad_pws.append(valid_pws[~char_check],ignore_index=True)
valid_pws = valid_pws[char_check]

# Rule 3: Must not contain the phrase password (case insensitive)
banned_phrases = valid_pws['password'].str.contains('password', case=False) 
bad_pws = bad_pws.append(valid_pws[banned_phrases],ignore_index=True)
valid_pws = valid_pws[~banned_phrases]

# Rule 4: Must not contain the user's first or last name
# Extracting first and last names into their own columns
valid_pws['first_name'] = valid_pws['username'].str.extract('(^\w+)', expand = False)
valid_pws['last_name'] = valid_pws['username'].str.extract('(\w+$)', expand = False)
# Iterate over DataFrame rows
for i, row in valid_pws.iterrows():
    if row.first_name in row.password.lower() or row.last_name in row.password.lower():
        valid_pws = valid_pws.drop(index=i)
        bad_pws = bad_pws.append(row,ignore_index=True)
# Note this could be done more efficiently with a lambda function

# Answering the questions
bad_pass = round(bad_pws.shape[0] / logins.shape[0], 2)
print("Percentage of users with invalid passwords", bad_pass)
email_list = bad_pws['username'].sort_values()
print(email_list)
