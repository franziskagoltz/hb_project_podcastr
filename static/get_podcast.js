"use strict";

// keepping track of global data
var data = {"queue": null,
        "offset": 0,
        "globalVarCategory": null,
        };

// grabbing podcasts from the databse based on what category is selected and 
// populating the queue
function getPodcasts(offset, category) {

    console.log(category);

    // querying the database and grabbing two podcasts from the specified category
    $.get("/get-content.json", {"offset": data.offset, "category": data.globalVarCategory}, function(results) {

        // grabbing the data we returned from the server side
        var episodes = results["data"];

        // add episodes to the queue
        for (var i = 0; i < episodes.length; i++) {
            data.queue.push(episodes[i]);
        }

        // play podcast
        playNextPodcast();
    });
}

// checking the length of the queue after every podcast played
function checkQueue(category) {

    // if queue is low, repopulate
    if (data.queue.length <= 1) {
        data.offset += 2;
        getPodcasts(data.offset, data.globalVarCategory);
    }
    // otherwise play next podcast
    else {
        playNextPodcast();
    }
}

// setting a golabl variable because we need access to it from a event handler
var episode;

// playing the next podcast in the queue
function playNextPodcast() {

    // grabbing an episode from the queue
    episode = data.queue.shift();

    var url = episode.play_url;
    var title = episode.title;
    var author = episode.author;

    // updating the values in the html with details from the current episode
    $("#player").attr("src", url);
    $("#podcast-description").html(title);
    $("#station").html(author);
}

// start playing a podcast from a new category
function playNewCategory(category) {
    data.globalVarCategory = category;
    console.log(data.globalVarCategory);

    data.queue = [];
    data.offset = 0;
    console.log("setting queue to empty");
    getPodcasts(data.offset, data.globalVarCategory);
}

// eventhandler on finishing an episode
$("#player").on("ended", function() {

    // send the id of the episode to the server
    $.post("/record", {"data": episode.podcast_id});
    // check queue and play new podcast
    checkQueue(data["globalVarCategory"]);
    // playNextPodcast();
});


// eventhandler on skip
$("#skip").on("click", function() {
    console.log("skipping");
    $.post("/record", {"data": episode.podcast_id});
    checkQueue(data.globalVarCategory);
});



// OLD COMMENTS/TRIES

    // console.log(queue);
    // setTimeout(playNextPodcast, 3000);
    // if (queue.length > 1){
    //     playNextPodcast();
    // }
    // podcasts(offset);


    // podcasts(offset, function(){
    //     playNextPodcast();
    // });

// setTimeout(playNextPodcast(), 10000);

// var p1 = new Promise(function(resolve, reject) {
//         resolve(podcasts(offset));
//     })
//     p1.then(function(value) {
//         console.log(value);
//         playNextPodcast();
//     });

    // var podcastQueuePromise = new Promise(function(resolve, reject) {
    //     console.log(queue);
    //     podcasts(offset);
    //     console.log(queue);
    // } );
    // podcastQueuePromise.then(
    //     playNextPodcast());
    //     console.log(queue);
    // console.log(queue);
    // podcastQueuePromise.then( function() {console.log(queue);})
    // playNextPodcast();

// new Promise( /* executor */ function(resolve, reject) { ... } );

// evtlistener: on category change do func() {
//     empty queue
//     checkQueue
//     playPod()
// }


// eventlistener on ended -- make new ajax call to repleneish queue and play next item from queue (or random list)


// if there several items in queue - grab a random one and make that the play_url. make sure to pop from list to decrease the queue

//     when do i want to make new call??

// else:
//     where is the offset (from the browser (hidden value in html))
//     pass that into ajax call - to to get podcast.json route
//     add updated limit and offset 

//     new query in db

//     can pass data also via get request

// var url = "https://play.podtrac.com/npr-510289/npr.mc.tritondigital.com/NPR_510289/media/anon.npr-mp3/npr/pmoney/2016/10/20161021_pmoney_podcast102116.mp3?orgId=1&d=1140&p=510289&story=498879523&t=podcast&e=498879523&ft=pod&f=510289"

// $("#player").attr("src", url)



        // var url = episodes[i].play_url;
        // var title = episodes[i].title;
        // var author = episodes[i].author;

        // console.log(url);
        // console.log(title);

        // // out of for loop. add event listemer on click : list of object
        // $("#player").attr("src", url);
        // $("#podcast-description").append(title);
        // $("#station").append(author);