# Hashtag Partisianship - Visualizing Twitter Politics

Hashtags are a functional tag used in social media, indexing tweets and messages based on a specific set of characters, from \#lovewins to \#fakenews. In doing so, it tags the digital content to a specific topic, making it easily accessible to people looking for similar results. This project was to see if we could look into the politics behind the hashtags, and see if we can find the bias and motivations behind the keywords themselves.

Using a database of [tweets by parliamentarians around the world](http://twitterpoliticians.org/download#), we wanted to analyze if we could determine the politican alignment of a specific hashtag based on the partisianship of the politicians that tweet it, along with adjacent hashtags on related subjects.

Our project was created using Python, specifically the NetworkX libraries for generating the graphs and tkinter for displaying it.

More information can be found in our write-up report PDF.

### Obtaining the data-sets:
After downloading the files from TwitterPoliticians, you can use [this hydrator](https://github.com/DocNow/hydrator) in order to create the dataset of the entire tweets (the hydrated data-set is 40GB large!)

### Running the program.

Make sure you've installed the required libraries specified in requirements.txt.

Then, ensuring that the data-set is put into the same directory as main.py, all you have to do is run main.py.

Depending on your machine, this should take approximately 20 minutes to process the entire 40GB file of hydrated tweets.

Afterwards, there's a GUI will open in your browser, with a graph of all the vertices. You can select an individual vertice with the drop-down menu.

The size of the hashtag node is correlated with how popular it is (how often it's tweeted by many people), and the adjacency of the nodes indicate if the hashtags are strongly correlated (often appear together such as #Veterans and #VeteranDay), or weakly correlated (one appears a lot more than another such as #Trump with #DACA)


