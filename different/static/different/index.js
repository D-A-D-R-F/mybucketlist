var list_of_activities = ['Go for a run' , 'Prank call a friend' ,
'Do a jigsaw puzzle' , 'Solve the wordle of the day' , 'Go for a hike' , 'Visit a museum' , 
'Learn a new programming language' , 'Follow a random youtube channel' , 'Make an origami bird' , 'Take a nap'
, 'Play charades' , 'Watch a movie' , 'Meet up with friends' , 'Play a sport',
'Call a family member' , 'Make paper boats' , 'Write a parody of your favourite song' , 'Decorate a hat' , 'Read a newspaper' , 'Discover a new band' , 
'Make a family history book' , 'Make a list of ideas for other people\'s birthdays' , 
'Video Chat with someone.' , 'Learn a new language.' , 'Read a book.' , 'Try a food you don\'t like' , 'Hold a video game tournament with some friends' , 
'Text a friend you haven\'t talked to in a long time' , 'Learn to sew on a button' , 'Volunteer and help out at a senior center' , 
'Rearrange and organize your room' , 'Listen to a new music genre' , 'Write a song' , 'Write a short story']




random_no = Math.floor((Math.random() * 13) + 1);
document.getElementById("res").innerHTML = list_of_activities[random_no]


var generate_btn = document.getElementById("generate-btn").onclick = function generate_random(){
    random_no = Math.floor((Math.random() * 13) + 1);
    document.getElementById("res").innerHTML = list_of_activities[random_no]

}



