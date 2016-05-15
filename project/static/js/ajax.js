var Ajax = function(){
    var self = this;
    if(instance === undefined){
        var instance = self;
    }
    return instance;
}


Ajax.prototype.get = function(url, data, success, error){
    var self = this;
    data = data || {};
    success = success || function(){};
    error = error || function(){};
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        success: success,
        error: error,
        dataType: 'json',
        contentType: 'json'
    });
}


Ajax.prototype.post = function(url, data, success, error){
    var self = this;
    data = data || {};
    data = JSON.stringify(data);
    success = success || function(){};
    error = error || function(){};
    self.get_token();
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: success,
        error: error,
        dataType: 'json',
        contentType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", self.csrftoken);
        }
    });
}


Ajax.prototype.get_token = function(){
    var self = this;
    self.csrftoken = Cookies.get('csrftoken');
    if(self.csrftoken === undefined){
        throw "Missing CSRF token";
    }
}
