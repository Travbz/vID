# Welcome to vID

## Summary

<p>
vID is a string slicing tool that slices the words in a name-string,
concatonates the sub-strings, hashes the unique sub-strings,
and concatonates a few numbers generated from the sub-strings unique hash.
If you enter a string the same way each time, it will return the same unique id. 
If a string does not contain enough sub-strings to satisfy the conditions, placeholder 'x' is used.

vID comes in two flavors. One flavor is a desktop app that slices a single name and returns a unique id. 
The other is a .ipynb file that reads a csv or xlsx file, and converts an entire column of names to unique id's.    
Contributions and forks very welcomed. Please star this repo if you like this project :)
</p>

## The desktop name converter:
![Demo Image]('vID_demo.png')

## Installation

<p>
Details coming soon, still configuring the .exe

</p>

## The docs
### vID:
<ol>
<li>Converts inputs to uppercase</li>
<li>Removes all non alpha or numeric characters </li>
<li>Counts the letters in the name</li>
<li>Counts the words in the name</li>
<li>slices the name according to the following convention: </li>
<ol>
<li>If the name is one word, it takes the first 8 characters in the name.</li>
<li>If the name has >=2 words: </li>
<ol>
<li>Grabs the first four characters in the first word of the name, or any characters present in that range(<= 4 characters).</li>
<li>After slicing the first word it passes to the next word and takes the first two characters or whatever is present <= 2 characters</li>
<li> If another word exists it will slice the first two characters present or whatever is present <= 2 characters</li>
<li>It repeats this process until it slices a total of 8 characters</li>
</ol>
</ol>
<li>After 8 characters have been sliced they are passed as a key to a hashing function which returns their hash value</li>
<ls>The 2nd to the 4th hash values are concatonated onto the 8 character unique string id:</ls>
<li>If the name was <=7 characters either before or after slicing, a lowercase placeholder value was added for readability</li>
<ol>
<li>In this instance I chose "x" as a placeholder but that can be easily changed in the script</li>
<ol>
</ol>

### To change the placeholder update the code below. Replace the 'x' in " unique_key += 'x' " with the character you want as your placeholder.
### The code is on line 30 in the "id_4_csv.ipynb" file.

### It looks like this:
```python
    if len(unique_key) <= 8:
        unique_key += 'x' * (8 - len(unique_key))
```

## To use the csv parser you must make a few changes to this code to reflect the path and name of your file, and the name of your column.

<ol>
<ls>You must change the name of the "read_excel('company.csv')" to the filepath and/or name of your excel file</ls>
<ol>
<ls>You mush also change some code in this file to point at the column you have that contains your names.</ls>
<ol>
<ls>Cell 4, line 5: "keys_list.append(generate_unique_id(row[" <Your name column's name here>  "]))" is the location of that command</ls>
</ol>
</ol>
<ls>If your file is a csv you need to comment-out the last two lines in the first cell.</ls>
</ol>

### Code to comment out if you have a csv:
```python
    # change 'company.xlsx' to 'path_of_your_file/the_name_of_your_file.xlsx'
    df = pd.read_excel('company.xlsx')
    df.to_csv('company.csv', mode = 'w', index=False)

```
### If you have a csv, comment-out the code above but change the name of the file in the csv_reader below to reflect your file path and name:

```python
#   example = pd.read_csv('C:/user/customers/customer.csv')
    df = pd.read_csv('company.csv')
```
### Once you have done that all thats left is to change the script to point at your names column:

```python
        keys_list.append(generate_unique_id(row[" <Your name column's name here>  "]))
```
### After youve updated the name column you can run the cells and generate unique Ids for every value in your names column.
