
function isValidISBN(isbn) {
    return isbn.match(/^\d{13}$/) !== null;
}

function searchBookDaum(isbn) {
    var promise = jQuery.Deferred();

    $.getJSON("http://apis.daum.net/search/book?callback=?",
        {q: isbn,
         searchType: "isbn",
         output: "json",
         apikey: "e687f4cfe38cb4916caa8240e7c8588a6269c21c"}
    ).done(function(content) {
        promise.resolve(content.channel.item[0].title);
    });

    return promise;
}

function coverImageKyobo(isbn) {
    return "http://image.kyobobook.co.kr/images/book/xlarge/" + isbn.substr(isbn.length - 3) + "/x" + isbn + ".jpg"
}

BookStore = {
    maybeGetTitle: searchBookDaum,
    getCoverImage: coverImageKyobo
}

$(function() {
    $("form.add-book input#id_isbn").bind('input', function() {
        var self = $(this);
        var isbn = self.val();

        if (isValidISBN(isbn)) {
            var form = $(self.closest("form"));
            
            var cover_url_field = form.find("#id_cover_url");
            cover_url_field.val(BookStore.getCoverImage(isbn));
            cover_url_field.trigger('input');

            var title_field = form.find("#id_title");
            BookStore.maybeGetTitle(isbn).done(function(title) {
                title_field.val(title);
            });
        }
    });

    $("form.add-book input#id_cover_url").bind('input', function() {
        var self = $(this);
        $(".cover img").attr("src", self.val());
    });

});
