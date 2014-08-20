
function isValid(isbn) {
    return isbn.match(/^\d{13}$/) !== null;
}

function searchBook(isbn) {
    return $.getJSON("http://apis.daum.net/search/book?callback=?",
            {q: isbn,
             searchType: "isbn",
             output: "json",
             apikey: "e687f4cfe38cb4916caa8240e7c8588a6269c21c"})

}

$(function() {
    $("form.add-book input#id_isbn").bind('input', function() {
        var self = $(this);
        var isbn = self.val();

        if (isValid(isbn)) {
            var form = $(self.closest("form"));
            
            var cover_url_field = form.find("#id_cover_url");
            cover_url_field.val("http://image.kyobobook.co.kr/images/book/xlarge/" + isbn.substr(isbn.length - 3) + "/x" + isbn + ".jpg");
            cover_url_field.trigger('input');

            var title_field = form.find("#id_title");

            searchBook(isbn).done(function(content) {
                title_field.val(content.channel.item[0].title);
            });
        }
    });

    $("form.add-book input#id_cover_url").bind('input', function() {
        var self = $(this);
        $(".cover img").attr("src", self.val());
    });

});
