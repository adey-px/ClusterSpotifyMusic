
/* functionality to play audio songs using mediaelementplayer library  */

let playAudio = {    
        init: function() {        
        var $that = this;        
            $(function() {            
                $that.components.media();        
            });    
        },
        components: {        
            media: function(target) {            
                let media = $('audio.player');            
                if (media.length) {                
                    media.mediaelementplayer({                    
                        audioHeight: 40,
                        features : ['playpause', 'current', 'duration', 'progress', 'volume'],
                        alwaysShowControls      : true,
                        timeAndDurationSeparator: '<span></span>',            
                    });            
                }        
            },
                
        },
    };
    playAudio.init();