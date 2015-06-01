function tweet_bind() {
    if ($.trim($(this).val()) == "") {
        $("#id-tweet-button").addClass("disabled");
    } else {
        $("#id-tweet-button").removeClass("disabled");
    }
}

function tweet() {
    $("#id-loader").removeClass("hide");
    $("#id-tweet-button").addClass("disabled");
    var tweet_text = $("#id-tweet-text").val();
    $.post("/tweet", {'tweet_text': tweet_text}, function(data) {
        $("#id-loader").addClass("hide");
        $("#id-tweet-text").val("");
        if(data['status']) {
            render_post(data['recent_tweets']);
        } else {
            alert(data['msg']);
        }
    });
}

function render_post(data) {
    $("#id-recent-tweets").html("");
    
    $.each(data, function(index, value) {
        $("#id-recent-tweets").append("<pre>" + value + "</pre>");
    });
    
}
