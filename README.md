# Sean's final project proposal

**Technologies**

+ Python, Numpy, Pandas & PostgreSQL, Flask
+ Tensorflow 2
+ SciKit learn
+ Glove

**Key concepts**

+ NLP - Natural Language processing
+ NERC - Named Entity Recognition and Classification
+ Embedding
+ Categorical cross-entropy

**Dataset**

The dataset from my business:
  + ****Stories****
    + Size
      + 142,629 rows
    + Columns
      + story_id, title_text, intro_text, body_text
    + ***Observation***
      + A lot of HTML needs removing from stories before training.
+ ****Taggings****
    + Size = 406,771 rows
    + Columns = story_id, tag_id
+ ****Tags****
    + Size
      + 11,507
    + Columns
      + Tag id, Tag name
    + ***Observation***
      + A lot of tags only have one related story

**Steps:**
+ ****Preprocessing****
  + Combine titles, intro text and body text from each training story
  + Remove HTML tags
  + Remove stop words
  + Apply ‘Named entity recognition’ to reduce the size of each story to just keywords
+ ****Training****
  + Train the model with the reduced story corpus and the tag features
  + Test and fine-tune
  + Go into production
  + Estimate the time and money savings

**Objectives**
+ Tag all stories with less than 5 tags (About 42,000)
+ Have a live tagging system when editors are inputting stories
+ Go into production
