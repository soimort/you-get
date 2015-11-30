(function() {
    var P, z, B, G, Q, R, S;
    function A(b) {
        var d = document.createElement("script");
        d.type = "text/javascript";
        d.src = b;
        document.getElementsByTagName("head")[0].appendChild(d)
    }
    function Ba(b) {
        if (!b) return "";
        var b = b.toString(),
        d,
        c,
        g,
        i,
        f,
        j = [ - 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
        i = b.length;
        g = 0;
        for (f = ""; g < i;) {
            do d = j[b.charCodeAt(g++) & 255];
            while (g < i && -1 == d);
            if ( - 1 == d) break;
            do c = j[b.charCodeAt(g++) & 255];
            while (g < i && -1 == c);
            if ( - 1 == c) break;
            f += String.fromCharCode(d << 2 | (c & 48) >> 4);
            do {
                d = b.charCodeAt(g++) & 255;
                if (61 == d) return f;
                d = j[d]
            } while ( g < i && - 1 == d );
            if ( - 1 == d) break;
            f += String.fromCharCode((c & 15) << 4 | (d & 60) >> 2);
            do {
                c = b.charCodeAt(g++) & 255;
                if (61 == c) return f;
                c = j[c]
            } while ( g < i && - 1 == c );
            if ( - 1 == c) break;
            f += String.fromCharCode((d & 3) << 6 | c)
        }
        return f
    }
    function L(b, d) {
        for (var c = [], g = 0, i, f = "", j = 0; 256 > j; j++) c[j] = j;
        for (j = 0; 256 > j; j++) g = (g + c[j] + b.charCodeAt(j % b.length)) % 256,
        i = c[j],
        c[j] = c[g],
        c[g] = i;
        for (var m = g = j = 0; m < d.length; m++) j = (j + 1) % 256,
        g = (g + c[j]) % 256,
        i = c[j],
        c[j] = c[g],
        c[g] = i,
        f += String.fromCharCode(d.charCodeAt(m) ^ c[(c[j] + c[g]) % 256]);
        return f
    }
    function M(b, d) {
        for (var c = [], g = 0; g < b.length; g++) {
            for (var i = 0,
            i = "a" <= b[g] && "z" >= b[g] ? b[g].charCodeAt(0) - 97 : b[g] - 0 + 26, f = 0; 36 > f; f++) if (d[f] == i) {
                i = f;
                break
            }
            c[g] = 25 < i ? i - 26 : String.fromCharCode(i + 97)
        }
        return c.join("")
    }
    function Ca(b) {
        function d(b, d) {
            return b << d | b >>> 32 - d
        }
        function c(b) {
            var d = "",
            e, g;
            for (e = 7; 0 <= e; e--) g = b >>> 4 * e & 15,
            d += g.toString(16);
            return d
        }
        var g, i, f = Array(80),
        j = 1732584193,
        m = 4023233417,
        l = 2562383102,
        n = 271733878,
        q = 3285377520,
        o,
        t,
        r,
        p,
        v,
        b = function(b) {
            for (var b = b.replace(/\r\n/g, "\n"), d = "", c = 0; c < b.length; c++) {
                var e = b.charCodeAt(c);
                128 > e ? d += String.fromCharCode(e) : (127 < e && 2048 > e ? d += String.fromCharCode(e >> 6 | 192) : (d += String.fromCharCode(e >> 12 | 224), d += String.fromCharCode(e >> 6 & 63 | 128)), d += String.fromCharCode(e & 63 | 128))
            }
            return d
        } (b);
        o = b.length;
        var w = [];
        for (g = 0; g < o - 3; g += 4) i = b.charCodeAt(g) << 24 | b.charCodeAt(g + 1) << 16 | b.charCodeAt(g + 2) << 8 | b.charCodeAt(g + 3),
        w.push(i);
        switch (o % 4) {
        case 0:
            g = 2147483648;
            break;
        case 1:
            g = b.charCodeAt(o - 1) << 24 | 8388608;
            break;
        case 2:
            g = b.charCodeAt(o - 2) << 24 | b.charCodeAt(o - 1) << 16 | 32768;
            break;
        case 3:
            g = b.charCodeAt(o - 3) << 24 | b.charCodeAt(o - 2) << 16 | b.charCodeAt(o - 1) << 8 | 128
        }
        for (w.push(g); 14 != w.length % 16;) w.push(0);
        w.push(o >>> 29);
        w.push(o << 3 & 4294967295);
        for (b = 0; b < w.length; b += 16) {
            for (g = 0; 16 > g; g++) f[g] = w[b + g];
            for (g = 16; 79 >= g; g++) f[g] = d(f[g - 3] ^ f[g - 8] ^ f[g - 14] ^ f[g - 16], 1);
            i = j;
            o = m;
            t = l;
            r = n;
            p = q;
            for (g = 0; 19 >= g; g++) v = d(i, 5) + (o & t | ~o & r) + p + f[g] + 1518500249 & 4294967295,
            p = r,
            r = t,
            t = d(o, 30),
            o = i,
            i = v;
            for (g = 20; 39 >= g; g++) v = d(i, 5) + (o ^ t ^ r) + p + f[g] + 1859775393 & 4294967295,
            p = r,
            r = t,
            t = d(o, 30),
            o = i,
            i = v;
            for (g = 40; 59 >= g; g++) v = d(i, 5) + (o & t | o & r | t & r) + p + f[g] + 2400959708 & 4294967295,
            p = r,
            r = t,
            t = d(o, 30),
            o = i,
            i = v;
            for (g = 60; 79 >= g; g++) v = d(i, 5) + (o ^ t ^ r) + p + f[g] + 3395469782 & 4294967295,
            p = r,
            r = t,
            t = d(o, 30),
            o = i,
            i = v;
            j = j + i & 4294967295;
            m = m + o & 4294967295;
            l = l + t & 4294967295;
            n = n + r & 4294967295;
            q = q + p & 4294967295
        }
        v = c(j) + c(m) + c(l) + c(n) + c(q);
        return v.toLowerCase()
    }
    function C(b, d) {
        if ("js" == d) {
            var c = document.createElement("script");
            c.setAttribute("type", "text/javascript");
            c.setAttribute("src", b)
        } else "css" == d && (c = document.createElement("link"), c.setAttribute("rel", "stylesheet"), c.setAttribute("type", "text/css"), c.setAttribute("href", b));
        "undefined" != typeof c && document.getElementsByTagName("head")[0].appendChild(c)
    }
    function $() {
        return f.isAndroid ? f.isAndroid4 ? "adr4": "adr": f.isIPHONE ? "iph": f.isIPAD ? "ipa": f.isIPOD ? "ipo": "oth"
    }
    function D(b) {
        return f.isIPAD && 0 <= window.location.href.indexOf("v.youku.com") ? "x-player": 200 >= b ? "x-player x-player-200": 300 >= b ? "x-player x-player-200-300": 660 >= b ? "x-player x-player-300-660": 800 >= b ? "x-player x-player-660-800": "x-player"
    }
    window.console = {};
    window.console.log = function() {};
    debug = {
        log: function(b) {
            null != document.getElementById("debug") && (document.getElementById("debug").innerHTML += b + " | ")
        }
    };
    var c = {},
    H = {},
    f = {
        playerType: "",
        uniplayerUrl: "http://passport-log.youku.com/logsys/logstorage/append?project=uniplayer&log=",
        MPIECEURL: "http://passport-log.youku.com/logsys/logstorage/append?project=mpiece&log=",
        userCache: {
            a1: "4",
            a2: "1"
        },
        playerState: {
            PLAYER_STATE_INIT: "PLAYER_STATE_INIT",
            PLAYER_STATE_READY: "PLAYER_STATE_READY",
            PLAYER_STATE_AD: "PLAYER_STATE_AD",
            PLAYER_STATE_PLAYING: "PLAYER_STATE_PLAYING",
            PLAYER_STATE_END: "PLAYER_STATE_END",
            PLAYER_STATE_ERROR: "PLAYER_STATE_ERROR"
        },
        playerCurrentState: "PLAYER_STATE_INIT",
        Log: function(b, d) {
            var c = document.createElement("img");
            d && c.addEventListener("error", d, !1);
            c.src = b + "&r_=" + Math.floor(1E4 * Math.random());
            c.id = "youku-uniplayer-stat"
        },
        isNeedAdrTrick: function() {
            return f.isAndroid && !f.adrPlayTrick && !f.isHTC && f.isNeedFrontAd && !f.isVIVO
        },
        adrInvalidPauseCheck: function(b) {
            var d = b.currentTime,
            c = 0,
            g = !1;
            f.adrPlayTrick = !0;
            b.pause();
            b.play();
            setInterval(function() {
                b.currentTime == d && !g ? (c++, b.play(), 0 == c % 10 && (b.load(), b.play())) : g = !0
            },
            1E3)
        },
        sendErrorReport: function(b) {
            var d = {},
            e = "",
            e = f.isIPAD ? "xplayer_ipad": f.isIPHONE ? "xplayer_iphone": "xplayer_android";
            d.m = e;
            d.ec = b;
            e = "";
            1E3 == b && (e = c.v.data.error.code);
            d.gc = e;
            d.u = encodeURIComponent(window.location.href);
            d.v = c.videoInfo ? c.videoInfo._sid: "";
            d.ct = c.v ? c.v.data ? c.v.data.video ? c.v.data.video.category_id: "": "": "";
            d.hd = f.hd ? f.hd: 0;
            c.v && c.v.data.network && (d.a = c.v ? c.v.data.network.area_code + "|" + c.v.data.network.dma_code: "");
            b = "";
            c.initConfig.vvlogconfig && c.initConfig.vvlogconfig.pvid && (b = c.initConfig.vvlogconfig.pvid);
            d.pid = b;
            f.Log("http://v.l.youku.com/perror?" + q(d))
        },
        uniReport: function(b) {
            b.partner = c.initConfig.client_id;
            b.os = encodeURI(f.os);
            b.mios = f.isMobileIOS;
            b.adrd4 = f.isAndroid4;
            b.mobile = f.isMobile;
            b.adrpad = f.isAndroidPad; ! 1 == b.mobile && (b.ua = encodeURI(navigator.userAgent.replace(/[\/\+\*@\(\)\,]/g, "")));
            b.version = "2015/11/2510:21:25".replace(/[-: ]/g, "");
            f.Log(f.uniplayerUrl + u(b))
        },
        Load: function(b, d) {
            if ("js" == d) {
                var c = document.createElement("script");
                c.setAttribute("type", "text/javascript");
                c.setAttribute("src", b)
            } else "css" == d && (c = document.createElement("link"), c.setAttribute("rel", "stylesheet"), c.setAttribute("type", "text/css"), c.setAttribute("href", b));
            "undefined" != typeof c && document.getElementsByTagName("head")[0].appendChild(c)
        },
        showError: function(b, d) {
            var e = c.get("#x-player");
            e.innerHTML = d ? d: "\u8be5\u89c6\u9891\u683c\u5f0f\u7279\u6b8a\uff0c\u8bf7\u5728PC\u4e0a\u89c2\u770b";
            e.style.textAlign = "center";
            e.style.color = "white";
            e.style.lineHeight = e.offsetHeight + "px";
            if (c.playerEvents && c.playerEvents.onPlayError) c.playerEvents.onPlayError(d ? d: "\u8be5\u89c6\u9891\u683c\u5f0f\u7279\u6b8a\uff0c\u8bf7\u5728PC\u4e0a\u89c2\u770b")
        }
    }; (function() {
        var b = document.createElement("video"),
        d = {
            MP4: "video/mp4",
            OGG: "video/ogg",
            WEBM: "video/webm"
        },
        c = {
            isWin: "Win",
            isMac: "Mac",
            isSafari: "Safari",
            isChrome: "Chrome",
            isIPAD: "iPad",
            isIPAD7: "iPad; CPU OS 7",
            isIPHONE: "iPhone",
            isIPOD: "iPod",
            isLEPAD: "lepad_hls",
            isMIUI: "MI-ONE",
            isAndroid: "Android",
            isAndroid4: "Android 4.",
            isAndroid41: "Android 4.1",
            isSonyDTV: "SonyDTV",
            isBlackBerry: "BlackBerry",
            isMQQBrowser: "MQQBrowser",
            isMobile: "Mobile",
            isSamSung: "SAMSUNG",
            isHTC: "HTC",
            isLumia: "Lumia",
            isVIVO: "vivo",
            isWeixin: "MicroMessenger"
        };
        f.supportHTML5Video = !1;
        f.isIOS = !1;
        f.os = "";
        if (b.canPlayType) {
            f.supportHTML5Video = !0;
            for (var g in d) f["canPlay" + g] = b.canPlayType(d[g]) ? !0 : !1
        }
        for (var i in c) if ( - 1 !== navigator.userAgent.indexOf(c[i]) ? (f[i] = !0, f.os += c[i] + " ") : f[i] = !1, -1 !== navigator.userAgent.indexOf("Android")) b = navigator.userAgent.indexOf("Android"),
        b = navigator.userAgent.substr(b, 10),
        b > c.isAndroid4 && (f.isAndroid4 = !0, f.os += b + " ");
        f.isMobileIOS = f.isIPAD || f.isIPHONE || f.isIPOD;
        f.isIOS = f.isMobileIOS || f.isMac;
        f.isSupportH5M3U8 = f.isMobileIOS || f.isMac && f.isSafari && !f.isChrome || f.isLEPAD || f.isSonyDTV;
        f.isSupportH5MP4 = (f.isChrome || f.isIE10 || f.isAndroid41 || f.isAndroid4 || f.isLumia) && f.canPlayMP4;
        i = c = 0;
        try {
            if (document.all) {
                var h = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
                if (h) {
                    var c = 1,
                    j = h.GetVariable("$version");
                    parseInt(j.split(" ")[1].split(",")[0])
                }
            } else if (navigator.plugins && 0 < navigator.plugins.length && (h = navigator.plugins["Shockwave Flash"])) for (var c = 1,
            m = h.description.split(" "), h = 0; h < m.length; ++h) isNaN(parseInt(m[h])) || parseInt(m[h])
        } catch(l) {
            i = c = 1
        }
        f.isSupportFlash = c && !i;
        f.isMQQBrowser && (f.isSupportFlash = !1);
        f.isLumia && (f.isSupportFlash = !1);
        f.isPhone = f.isIPHONE || f.isIPOD || f.isAndroid && f.isMobile;
        f.isAndroidPad = f.isAndroid && !f.isMobile;
        f.isPad = f.isIPAD || f.isAndroidPad;
        f.isMobile = f.isIPAD || f.isIPHONE || f.isIPOD || f.isLEPAD || f.isMIUI || f.isAndroid4 || f.isSonyDTV || f.isLumia
    })();
    var T = function(b) {
        debug.log("canplay mp4 = " + f.canPlayMP4);
        c.initConfig = b;
        this._vid = b.vid;
        this._target = b.target;
        this._partnerId = b.partnerId;
        b.client_id && (this._partnerId = b.client_id); ! b.pkid && (!this._vid || !this._target || !this._partnerId) ? alert("[Fail]The params of {vid,target,client_id} are necessary !") : (this._events = b.events, c.playerEvents = b.events, f._target = this._target, this._paid = 0, null != b.paid && (this._paid = b.paid), this._id = b.id, null == this._id && (this._id = "youku-player"), f.playerId = this._id, this._width = b.width, this._height = b.height, this._expand = b.expand, null == b.width || null == b.height ? null == b.expand && (this._expand = 0) : null == b.expand && (this._expand = 1), this._prefer = b.prefer ? b.prefer.toLowerCase() : "flash", this._starttime = b.starttime, this._password = b.password, this._poster = b.poster, this._autoplay = eval(b.autoplay), this._canWide = b.canWide, this._showRelated = b.show_related, this._winType = b.wintype, this._pkid = b.pkid, this._pkpid = b.pkpid, this._pkurl = b.pkurl, this._playlistconfig = b.playlistconfig, this._isMobile = f.isMobile, this._isMobileIOS = f.isMobileIOS, c.isWeixin = f.isWeixin, "undefined" != typeof b.weixin && (c.isWeixin = !!b.weixin), this._playerType = "", c.mk = {},
        c.mk.a3 = "b4et", c.mk.a4 = "boa4")
    };
    T.prototype = {
        isSupportH5MP4: function() {
            return f.isSupportH5MP4
        },
        isSupportH5M3U8: function() {
            return f.isSupportH5M3U8
        },
        isSupportFlash: function() {
            return f.isSupportFlash
        },
        playerType: function() {
            if ("" != this._playerType) return this._playerType;
            this._playerType = "h5" == this._prefer ? this.isSupportH5M3U8() ? "h5m3u8": this.isSupportH5MP4() ? "h5mp4": this.isSupportFlash() ? "flash": "error": "flash" == this._prefer ? this.isSupportFlash() ? "flash": this.isSupportH5M3U8() ? "h5m3u8": this.isSupportH5MP4() ? "h5mp4": "error": "error";
            if (("h5m3u8" == this._playerType || "h5mp4" == this._playerType) && void 0 != this._pkid) this._playerType = "h5pk";
            return this._playerType
        },
        select: function() {
            debug.log("playerType = " + this.playerType());
            if (this.isThirdParty()) {
                var b = this;
                this.processThirdParty(function() {
                    b.selectHandler()
                })
            } else this.selectHandler()
        },
        selectHandler: function() {
            "h5m3u8" == this.playerType() ? this.selectH5M3U8() : "h5mp4" == this.playerType() ? this.selectH5MP4() : "h5pk" == this.playerType() ? this.selectH5PK() : "flash" == this.playerType() ? this.selectFlash() : this.selectDirectUrl();
            if (this._events && this._events.onPlayerReady) {
                var b = this._events.onPlayerReady;
                if ("h5" == f.playerType) var d = setInterval(function() {
                    if (document.getElementById(f.playerId)) {
                        f.playerCurrentState = f.playerState.PLAYER_STATE_READY;
                        debug.log(f.playerCurrentState);
                        clearInterval(d);
                        try {
                            n.appendItem("phase", "playerready"),
                            b()
                        } catch(c) {}
                    }
                },
                500);
                else "flash" == f.playerType && (d = setInterval(function() {
                    if (1 == H.swfLoaded) {
                        f.playerCurrentState = f.playerState.PLAYER_STATE_READY;
                        debug.log(f.playerCurrentState);
                        clearInterval(d);
                        try {
                            n.appendItem("phase", "playerready"),
                            b()
                        } catch(c) {}
                    }
                },
                500))
            }
        },
        selectH5MP4: function() {
            f.uniReport({
                mp4: 1
            });
            f.playerType = "h5";
            var b = this._h5player = new YoukuHTML5Player({
                id: this._id,
                vid: this._vid,
                partnerId: this._partnerId,
                parentBox: this._target,
                events: this._events,
                width: this._width,
                height: this._height,
                poster: this._poster,
                autoplay: this._autoplay,
                isMobile: this._isMobile,
                isMobileIOS: this._isMobileIOS,
                content: "mp4",
                wintype: this._winType,
                expand: this._expand,
                partner_config: this.partner_config,
                canWide: this._canWide ? this._canWide: 0
            });
            f.GetMP4OK = function(d, e) {
                n.appendItem("phase", "vinfo_mp4");
                b.startPlay(d, e);
                if (c.initConfig.events && c.initConfig.events.onMediaSrcOK) c.initConfig.events.onMediaSrcOK(c.defaultVideoType, e._videoSegsDic.streams[e._videoSegsDic.lang][c.defaultVideoType][0].src)
            };
            l.playlistconfig = this._playlistconfig;
            l.start(this._vid, this._password, "mp4")
        },
        selectH5M3U8: function() {
            f.uniReport({
                m3u8: 1
            });
            f.playerType = "h5";
            var b = {
                id: this._id,
                vid: this._vid,
                partnerId: this._partnerId,
                parentBox: this._target,
                events: this._events,
                width: this._width,
                height: this._height,
                poster: this._poster,
                autoplay: this._autoplay,
                isMobile: this._isMobile,
                isMobileIOS: this._isMobileIOS,
                content: "m3u8",
                wintype: this._winType,
                expand: this._expand,
                partner_config: this.partner_config,
                canWide: this._canWide ? this._canWide: 0
            };
            if (f.isIPHONE || f.isIPOD) b.playType = "directsrc";
            var d = new YoukuHTML5Player(b);
            this._h5player = d;
            f.GetM3U8OK = function(b, c) {
                n.appendItem("phase", "vinfo_m3u8");
                d.startPlay(b, c)
            };
            l.playlistconfig = this._playlistconfig;
            l.start(this._vid, this._password, "m3u8")
        },
        selectH5PK: function() {
            f.playerType = "h5";
            var b = {
                id: this._pkid,
                pid: this._pkpid,
                url: decodeURIComponent(this._pkurl),
                parentBox: this._target
            };
            this._h5player = new aa(b)
        },
        processThirdParty: function(b) {
            var d = new ba({
                client_id: c.initConfig.client_id,
                video_id: c.initConfig.vid,
                embsig: c.initConfig.embsig,
                refer: encodeURIComponent(window.location.href)
            }),
            e = this;
            d.addEventListener(Q,
            function(d) {
                debug.log("thirdparty res ok");
                e.partner_config = d.data;
                b()
            });
            d.addEventListener(R,
            function() {
                debug.log("thirdparty res error");
                b()
            });
            d.addEventListener(S,
            function() {
                debug.log("thirdparty res timeout");
                b()
            })
        },
        selectH5VTag: function() {
            f.playerType = "h5";
            var b = "http://v.youku.com/player/getM3U8/vid/" + this._vid + "/type/mp4/ts/" + parseInt((new Date).getTime() / 1E3),
            b = b + (this._password ? "/password/" + this._password: ""),
            b = '<video src="' + (b + "/v.m3u8") + '" controls width=' + this._width + " height=" + this._height + " id=" + this._id + " autohide=false " + (this._poster ? "poster=" + this._poster: "") + " " + (!0 == this._autoplay ? "autoplay=true": "") + "></video>";
            document.getElementById(this._target).innerHTML = b
        },
        isThirdParty: function() {
            if (void 0 != this._pkid) return ! 1;
            var b = c.initConfig.client_id;
            return null != b && 16 == (b + "").length ? !0 : !1
        },
        selectFlash: function() {
            f.uniReport({
                flash: 1
            });
            f.playerType = "flash";
            var b = {
                imglogo: this._poster || "",
                paid: this._paid,
                partnerId: c.initConfig.client_id
            };
            null != c.initConfig.firsttime && (b.firsttime = c.initConfig.firsttime);
            null != this._autoplay && (b.isAutoPlay = this._autoplay);
            null != c.initConfig.embsig && (b.embsig = c.initConfig.embsig);
            null != this._showRelated && (b.isShowRelatedVideo = this._showRelated);
            null != c.initConfig.password && (b.passwordstr = c.initConfig.password);
            null != c.initConfig.styleid && (b.styleid = c.initConfig.styleid);
            null != c.initConfig.vext && (b.vext = c.initConfig.vext);
            for (var d in c.initConfig.adconfig) b[d] = c.initConfig.adconfig[d];
            for (d in c.initConfig.flashconfig) b[d] = c.initConfig.flashconfig[d];
            d = "";
            this.isThirdParty() && (d = "/partnerid/" + this._partnerId);
            b.delayload && (d = "");
            var e = "";
            null != this._winType && "" != this._winType && (e = "/winType/" + this._winType);
            null != c.initConfig.pkid && (b.VideoIDS = c.initConfig.pkid);
            null != c.initConfig.pkpid && (b.pkpid = c.initConfig.pkpid);
            null != c.initConfig.pkurl && (b.pkurl = c.initConfig.pkurl);
            d = ca + "/player.php/sid/" + this._vid + d + e + "/v.swf";
            c.initConfig.flashsrc && (d = c.initConfig.flashsrc);
            null != c.initConfig.pkid && (d = "youkupaike.swf");
            b = q(b);
            document.getElementById(this._target).innerHTML = "<object type=application/x-shockwave-flash data= " + d + " width=100% height=100% id=" + this._id + "><param name=allowFullScreen value=true><param name=allowScriptAccess value=always><param name=movie value=" + d + "><param name=flashvars value=" + b + ">" + (c.initConfig.flashext || "") + "</object>";
            this._expand && (document.getElementById(this._target).style.width = this._width + "px", document.getElementById(this._target).style.height = this._height + "px")
        },
        selectDirectUrl: function(b) {
            b = b || "mp4";
            debug.log("select directsrc");
            f.uniReport({
                direct: 1
            });
            f.playerType = "directsrc";
            var d = new da({
                id: this._id,
                vid: this._vid,
                partnerId: this._partnerId,
                parentBox: this._target,
                events: this._events,
                width: this._width,
                height: this._height,
                poster: this._poster,
                autoplay: this._autoplay,
                isMobile: this._isMobile,
                isMobileIOS: this._isMobileIOS,
                content: b,
                playType: "directsrc",
                wintype: this._winType,
                expand: this._expand,
                canWide: this._canWide ? this._canWide: 0
            });
            this._h5player = d;
            l.playlistconfig = this._playlistconfig;
            l.start(this._vid, this._password, b,
            function(b, c) {
                d.startPlay(b, c)
            })
        },
        selectError_: function(b, d) {
            f.uniReport({
                error: 1
            });
            if (this._width || this._height) document.getElementById(this._target).style.width = this._width + "px",
            document.getElementById(this._target).style.height = this._height + "px";
            f.playerType = "error";
            f.showError(this._target, b, d)
        }
    };
    H.Player = function(b, d) {
        d.target = b;
        this.select = new T(d);
        this.select.select();
        this._player = ""
    };
    H.Player.prototype = {
        player: function() {
            return "" != this._player ? this._player: this._player = "h5" == f.playerType ? new ea(this.select._h5player) : "flash" == f.playerType ? new fa: "error"
        },
        resize: function(b, d) {
            this.player().resize(b, d)
        },
        currentTime: function() {
            return this.player().currentTime()
        },
        totalTime: function() {
            return this.player().totalTime()
        },
        playVideo: function() {
            this.player().playVideo()
        },
        startPlayVideo: function() {
            this.player().startPlayVideo()
        },
        pauseVideo: function() {
            this.player().pauseVideo()
        },
        seekTo: function(b) {
            this.player().seekTo(b)
        },
        hideControls: function() {
            this.player().hideControls()
        },
        showControls: function() {
            this.player().showControls()
        },
        playVideoById: function(b) {
            this.player().playVideoById(b)
        },
        switchFullScreen: function() {
            try {
                this.player().switchFullScreen()
            } catch(b) {}
        }
    };
    var fa = function() {
        this._player = document.getElementById(f.playerId)
    };
    fa.prototype = {
        resize: function(b, d) {
            this._player.style.width = b + "px";
            this._player.style.height = d + "px"
        },
        currentTime: function() {
            var b = this._player.getPlayerState().split("|");
            return 3 <= b.length ? b[2] : -1
        },
        totalTime: function() {
            var b = this._player.getPlayerState().split("|");
            return 4 <= b.length ? b[3] : -1
        },
        playVideo: function() {
            this._player.pauseVideo(!1)
        },
        pauseVideo: function() {
            this._player.pauseVideo(!0)
        },
        seekTo: function(b) {
            this._player.nsseek(b)
        },
        playVideoById: function(b) {
            this._player.playVideoByID(b)
        },
        hideControls: function() {
            this._player.showControlBar(!1)
        },
        showControls: function() {
            this._player.showControlBar(!0)
        }
    };
    Q = "openapiokyouku";
    S = "openapitimeoutyouku";
    R = "openapierror";
    var ba = function(b) {
        this._handler = {};
        window.partnerinfo = this;
        b.callback = "partnerinfo.parse";
        b = q(b);
        A("https://api.youku.com/players/custom.json?" + b);
        var d = this;
        setTimeout(function() {
            d._hasResp || d.dispatch({
                type: S
            })
        },
        2E3)
    };
    ba.prototype = {
        addEventListener: function(b, d) {
            this._handler[b] = d
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        parse: function(b) {
            this._hasResp = !0;
            null != b.error || 1 != b.status ? this.dispatch({
                type: R
            }) : this.dispatch({
                type: Q,
                data: b
            })
        }
    };
    var l = {},
    E = {},
    I = [];
    l.mp4srcs = [];
    l.start = function(b, d, c, g) {
        this._callback = g;
        if (null == this._callback) switch (this._type) {
        case "m3u8":
            this._callback = f.GetM3U8OK;
            break;
        case "mp4":
            this._callback = f.GetMP4OK;
            break;
        default:
            this._callback = f.GetM3U8OK
        }
        null != E[b] && null != E[b][c] ? (console.log("Cache Hit vid = " + b), this._callback(E[b][c].v, E[b][c].videoInfo)) : (this._vid = decodeURIComponent(b), this._password = d, this._type = c, this._videoInfo = null, this._url = "", this.mp4srcs = [], this.request())
    };
    l.cache = function() {
        E[l._vid] = {};
        E[l._vid][l._type] = {
            v: this._v,
            videoInfo: this._videoInfo
        }
    };
    l.getPlayListUrl = function() {
        var b = "http://play.youku.com/play/get.json?vid=" + decodeURIComponent(this._vid),
        b = b + "&ct=12",
        d;
        for (d in this.playlistconfig) b += "&" + d + "=" + this.playlistconfig[d];
        return b
    };
    l.error = function(b) {
        b || (b = 0);
        f.sendErrorReport(0);
        f.uniReport({
            error: b,
            vid: c.initConfig.vid
        });
        f.showError(c.config.parentBox, "\u8be5\u89c6\u9891\u6682\u65f6\u4e0d\u80fd\u64ad\u653e,\u8bf7\u4e0b\u8f7dAPP\u6216\u5728PC\u4e0a\u89c2\u770b", 320)
    };
    l.reportPlayListUep = function() {
        var b = (new Date).getTime() - this._plreqStartTime;
        I.push({
            type: "getplaylist",
            time: b
        })
    };
    l.response = function(b) {
        var d = b.data,
        e = d.stream;
        this.playlistError || (this.playlistOK = !0, this.reportPlayListUep(), (c.v = b) && d ? e && ("default" !== e[0].drm_type || "http" !== e[0].transfer_mode) ? this.error(1, b, d, e) : this.init(b) : this.error(1, b, d, e))
    };
    l.request = function() {
        this._url = this.getPlayListUrl();
        this._password && (this._url += "&pwd=" + encodeURI(this._password));
        this._password && (c.initConfig.client_id && c.config.partner_config && 1 == c.config.partner_config.status && 1 == c.config.partner_config.passless) && (this._url += "&cid=" + c.initConfig.client_id);
        this._url += "&callback=BuildVideoInfo.response";
        "" != c.getUCStr(this._vid) && (this._url += c.getUCStr(this._vid));
        this._plreqStartTime = (new Date).getTime();
        A(this._url);
        var b = this;
        setTimeout(function() {
            if (!b.playlistOK) {
                b.playlistError = true;
                f.sendErrorReport(2003);
                if (c.playerEvents && c.playerEvents.onPlayError) c.playerEvents.onPlayError("\u89c6\u9891\u4fe1\u606f\u51fa\u9519\uff0c\u8bf7\u5237\u65b0\u91cd\u8bd5");
                c.get("#x-player").innerHTML = "\u89c6\u9891\u4fe1\u606f\u51fa\u9519\uff0c\u8bf7\u5237\u65b0\u91cd\u8bd5";
                c.get("#x-player").style.color = "white";
                c.get("#x-player").style.textAlign = "center";
                c.get("#x-player").style.lineHeight = c.get("#x-player").offsetHeight + "px"
            }
        },
        15E3)
    };
    l.m3u8src = function(b) {
        c.password = this._password;
        return c.m3u8src_v2(this._vid, b)
    };
    l.total = function(b, d, e) {
        b = b[d][e];
        e = d = 0;
        if (c.v.data.controller && c.v.data.controller.html5_disable) d += parseInt(c.v.data.video.seconds);
        else for (var g = 0; g < b.length; g++) var i = b[g],
        d = d + parseInt(i.seconds),
        e = e + parseInt(i.size);
        return {
            totalTime: d,
            totalBytes: e
        }
    };
    l.cleanSrc = function() {
        for (var b = this._videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType], d = 0; d < b.length; d++) b[d].fyksrc = b[d].src,
        b[d].src = l.mp4srcs[d]
    };
    l.processError = function(b) {
        debug.log("playlist errorcode = " + b.error.code);
        var d = b.stream;
        if ( - 301 == b.error.code || -303 == b.error.code) {
            for (b = 0; b < d.length; b++) {
                d[b].audio_lang = "default";
                d[b].drm_type = "";
                d[b].logo = "";
                d[b].milliseconds_audio = 0;
                d[b].milliseconds_video = 0;
                d[b].kye = "";
                d[b].size = 0;
                d[b].stream_fileid = "0*0";
                d[b].subtitle_lang = "";
                for (var c = 0; c < d[b].segs.length; c++) d[b].segs[c].kye = "",
                d[b].segs[c].size = 0,
                d[b].segs[c].total_milliseconds_audio = 0,
                d[b].segs[c].total_milliseconds_video = 0
            }
            return ! 1
        }
        null == this._callback ? "m3u8" == this._type ? f.GetM3U8OK(this._v, {}) : f.GetMP4OK(this._v, {}) : this._callback(this._v, {});
        return ! 0
    };
    l.init = function(b) {
        this._v = b;
        var d = b.data,
        e = d.stream;
        if (!d.security || !d.security.encrypt_string || !d.security.ip) f.sendErrorReport(2004),
        f.showError(null, "\u6570\u636e\u89e3\u6790\u9519\u8bef");
        else if (!e && !d.error) f.showError(null, '\u8be5\u89c6\u9891\u6682\u4e0d\u80fd\u64ad\u653e <a href="http://m.youku.com/webapp/dl?app=youku&amp;source=webqr" title="\u4e0b\u8f7d\u4f18\u9177\u5ba2\u6237\u7aef" target="_blank"><button type="button" class="x-btn" style="background: #3bb4fc;text-align: center;color: #fff;border-radius: 1rem;">\u7528app\u89c2\u770b</button></a>');
        else {
            var g = L(M(c.mk.a3 + "o0b" + f.userCache.a1, [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), Ba(d.security.encrypt_string));
            if (2 > g.split("_").length) f.sendErrorReport(2004),
            f.showError(null, "\u6570\u636e\u89e3\u6790\u9519\u8bef");
            else {
                f.userCache.sid = g.split("_")[0];
                f.userCache.token = g.split("_")[1];
                if (null != d.error) {
                    if ( - 202 == d.error.code || -203 == d.error.code) f.sendErrorReport(4E3);
                    else {
                        if ( - 402 == d.error.code) {
                            f.sendErrorReport(2007);
                            f.showError(c.config.parentBox, "\u7528\u6237\u6ca1\u6709\u6743\u9650\u89c2\u770b");
                            return
                        }
                        f.sendErrorReport(1E3)
                    }
                    if (this.processError(d)) return
                }
                this._videoInfo = new ga(d, e, this._type);
                e = this._videoInfo._videoSegsDic;
                g = "";
                c.defaultLanguage == e.lang ? g = c.defaultLanguage: (g = e.lang, c.defaultLanguage = e.lang);
                var i = l.total(e.streams, g, e.typeArr[g][0]);
                this._videoInfo.totalTime = i ? i.totalTime: d.video.seconds;
                if ("m3u8" == this._type) c.defaultVideoType = "mp4",
                null != n.getItem("defaultVideoType") && (c.defaultVideoType = n.getItem("defaultVideoType")),
                -1 == b.data.stream[0].stream_type.indexOf(c.defaultVideoType) && (c.defaultVideoType = "mp4", -1 == b.data.stream[0].stream_type.indexOf("mp4") && (c.defaultVideoType = "flv")),
                debug.log("default = " + c.defaultVideoType),
                this._videoInfo.src = l.m3u8src(c.defaultVideoType),
                this.cache(),
                null == this._callback ? f.GetM3U8OK(this._v, this._videoInfo) : this._callback(this._v, this._videoInfo);
                else if ("mp4" == this._type) {
                    d = ["3gphd", "mp4", "flv"];
                    c.defaultVideoType = null;
                    for (i = 0; i < d.length; i++) if (e.streams[g][d[i]] && !("3gphd" == d[i] && 7200 < parseInt(b.seconds))) {
                        c.defaultVideoType = d[i];
                        break
                    }
                    debug.log("mp4 type=" + c.defaultVideoType);
                    c.defaultVideoType ? ("flv" == c.defaultVideoType && (f.Log(f.uniplayerUrl + u({
                        error: "flvonly",
                        vid: c.initConfig.vid
                    })), c.config.playType = "directsrc"), this.fetchDirectSrc(e.streams[g][c.defaultVideoType], e.streams[g]), this._tid = setInterval("checkSrc()", 500)) : this.error(2)
                }
            }
        }
    };
    l.getFileUrl = function(b) {
        var d = [];
        if (b) for (var c = 0; c < b.length; c++) d.push(b[c].src);
        return d
    };
    l.fetchDirectSrc = function(b, d) {
        this._fyks = urls = this.getFileUrl(b);
        if (this._v && this._v.data.trial) {
            for (var c = 0,
            c = 0; c < d.mp4.length && -1 !== d.mp4[c].k; c++);
            urls.length = c
        }
        for (c = 0; c < urls.length; c++) l.mp4srcs.push(urls[c])
    };
    var ga = function(b, d, c) {
        this._sid = f.userCache.sid;
        this._fileType = c;
        this._videoSegsDic = {};
        new ha;
        var c = [],
        g = [];
        g.streams = {};
        g.logos = {};
        g.typeArr = {};
        g.totalTime = {};
        for (var i = 0; i < d.length; i++) {
            for (var h = d[i].audio_lang, j = !1, m = 0; m < c.length; m++) if (c[m] == h) {
                j = !0;
                break
            }
            j || c.push(h)
        }
        for (i = 0; i < c.length; i++) {
            for (var l = c[i], h = {},
            j = {},
            n = [], m = 0; m < d.length; m++) {
                var p = d[m];
                if (l == p.audio_lang && this.isValidType(p.stream_type)) {
                    var o = this.convertType(p.stream_type),
                    q = 0;
                    "none" != p.logo && (q = 1);
                    j[o] = q;
                    var r = !1,
                    u;
                    for (u in n) o == n[u] && (r = !0);
                    r || n.push(o);
                    q = p.segs;
                    if (null != q) {
                        var v = [];
                        r && (v = h[o]);
                        for (r = 0; r < q.length; r++) {
                            var w = q[r];
                            if (null == w) break;
                            var s = {};
                            s.no = r;
                            s.size = w.size;
                            s.seconds = Number(w.total_milliseconds_video) / 1E3;
                            s.milliseconds_video = Number(p.milliseconds_video) / 1E3;
                            s.key = w.key;
                            s.fileId = this.getFileId(p.stream_fileid, r);
                            s.src = this.getVideoSrc(m, r, b, p.stream_type, s.fileId);
                            s.type = o;
                            v.push(s)
                        }
                        h[o] = v
                    }
                }
            }
            m = this.langCodeToCN(l).key;
            g.logos[m] = j;
            g.streams[m] = h;
            g.typeArr[m] = n
        }
        this._videoSegsDic = g;
        this._videoSegsDic.lang = this.langCodeToCN(c[0]).key
    },
    ha = function(b) {
        this._randomSeed = b;
        this.cg_hun()
    };
    ha.prototype = {
        cg_hun: function() {
            this._cgStr = "";
            for (var b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890",
            d = b.length,
            c = 0; c < d; c++) {
                var g = parseInt(this.ran() * b.length);
                this._cgStr += b.charAt(g);
                b = b.split(b.charAt(g)).join("")
            }
        },
        cg_fun: function(b) {
            for (var b = b.split("*"), d = "", c = 0; c < b.length - 1; c++) d += this._cgStr.charAt(b[c]);
            return d
        },
        ran: function() {
            this._randomSeed = (211 * this._randomSeed + 30031) % 65536;
            return this._randomSeed / 65536
        }
    };
    ga.prototype = {
        getFileId: function(b, d) {
            if (null == b || "" == b) return "";
            var c = b.slice(0, 8),
            g = d.toString(16);
            1 == g.length && (g = "0" + g);
            var g = g.toUpperCase(),
            i = b.slice(10, b.length);
            return c + g + i
        },
        isValidType: function(b) {
            return "3gphd" == b || "flv" == b || "flvhd" == b || "mp4hd" == b || "mp4hd2" == b || "mp4hd3" == b ? !0 : !1
        },
        convertType: function(b) {
            var d = b;
            switch (b) {
            case "m3u8":
                d = "mp4";
                break;
            case "3gphd":
                d = "3gphd";
                break;
            case "flv":
                d = "flv";
                break;
            case "flvhd":
                d = "flv";
                break;
            case "mp4hd":
                d = "mp4";
                break;
            case "mp4hd2":
                d = "hd2";
                break;
            case "mp4hd3":
                d = "hd3"
            }
            return d
        },
        langCodeToCN: function(b) {
            var d = "";
            switch (b) {
            case "default":
                d = {
                    key: "guoyu",
                    value: "\u56fd\u8bed"
                };
                break;
            case "guoyu":
                d = {
                    key: "guoyu",
                    value: "\u56fd\u8bed"
                };
                break;
            case "yue":
                d = {
                    key: "yue",
                    value: "\u7ca4\u8bed"
                };
                break;
            case "chuan":
                d = {
                    key: "chuan",
                    value: "\u5ddd\u8bdd"
                };
                break;
            case "tai":
                d = {
                    key: "tai",
                    value: "\u53f0\u6e7e"
                };
                break;
            case "min":
                d = {
                    key: "min",
                    value: "\u95fd\u5357"
                };
                break;
            case "en":
                d = {
                    key: "en",
                    value: "\u82f1\u8bed"
                };
                break;
            case "ja":
                d = {
                    key: "ja",
                    value: "\u65e5\u8bed"
                };
                break;
            case "kr":
                d = {
                    key: "kr",
                    value: "\u97e9\u8bed"
                };
                break;
            case "in":
                d = {
                    key: "in",
                    value: "\u5370\u5ea6"
                };
                break;
            case "ru":
                d = {
                    key: "ru",
                    value: "\u4fc4\u8bed"
                };
                break;
            case "fr":
                d = {
                    key: "fr",
                    value: "\u6cd5\u8bed"
                };
                break;
            case "de":
                d = {
                    key: "de",
                    value: "\u5fb7\u8bed"
                };
                break;
            case "it":
                d = {
                    key: "it",
                    value: "\u610f\u8bed"
                };
                break;
            case "es":
                d = {
                    key: "es",
                    value: "\u897f\u8bed"
                };
                break;
            case "po":
                d = {
                    key: "po",
                    value: "\u8461\u8bed"
                };
                break;
            case "th":
                d = {
                    key: "th",
                    value: "\u6cf0\u8bed"
                };
                break;
            case "man":
                d = {
                    key: "man",
                    value: "\u6696\u7537"
                };
                break;
            case "baby":
                d = {
                    key: "baby",
                    value: "\u840c\u7ae5"
                }
            }
            return d
        },
        getVideoSrc: function(b, d, e, g, i, h, j) {
            var m = e.stream[b];
            if (!e.video.encodeid || !g) return "";
            var b = {
                flv: 0,
                flvhd: 0,
                mp4: 1,
                hd2: 2,
                "3gphd": 1,
                "3gp": 0
            } [g],
            g = {
                flv: "flv",
                mp4: "mp4",
                hd2: "flv",
                mp4hd: "mp4",
                mp4hd2: "mp4",
                "3gphd": "mp4",
                "3gp": "flv",
                flvhd: "flv"
            } [g],
            l = d.toString(16);
            1 == l.length && (l = "0" + l);
            var n = m.segs[d].total_milliseconds_video / 1E3,
            d = m.segs[d].key;
            if ("" == d || -1 == d) d = m.key2 + m.key1;
            m = "";
            e.show && (m = e.show.pay ? "&ypremium=1": "&ymovie=1");
            e = "/player/getFlvPath/sid/" + f.userCache.sid + "_" + l + "/st/" + g + "/fileid/" + i + "?K=" + d + "&hd=" + b + "&myp=0&ts=" + n + "&ypp=0" + m;
            i = encodeURIComponent(J(L(M(c.mk.a4 + "poz" + f.userCache.a2, [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), f.userCache.sid + "_" + i + "_" + f.userCache.token)));
            e = e + ("&ep=" + i) + "&ctype=12&ev=1" + ("&token=" + f.userCache.token);
            e += "&oip=" + c.v.data.security.ip;
            return "http://k.youku.com" + (e + ((h ? "/password/" + h: "") + (j ? j: "")))
        }
    };
    var ea = function(b) {
        this._player = document.getElementById("youku-html5player-video");
        null == this._player && (this._player = document.getElementById("youku-html5player-video-0"));
        this._oplayer = b
    };
    ea.prototype = {
        resize: function(b, d) {
            this._oplayer.resize(b, d)
        },
        currentTime: function() {
            return this._player.currentTime
        },
        totalTime: function() {
            return this._player.duration
        },
        playVideo: function() {
            this._oplayer.play()
        },
        startPlayVideo: function() {
            if (f.isNeedFrontAd) this._oplayer.controls.onVideoBtnTouchEnd();
            else this._oplayer.controls.onVideoBtnClick()
        },
        pauseVideo: function() {
            this._player.pause()
        },
        seekTo: function(b) {
            try {
                this._player.currentTime = b
            } catch(d) {}
        },
        playVideoById: function(b, d) {
            debug.log("YKH5Player playVideoByid");
            var e = this._oplayer;
            c.config.autoplay = !0;
            c.config.vid = b;
            l.start(b, d, c.config.content,
            function(b, d) {
                e.startPlay(b, d)
            })
        },
        hideControls: function() {
            this._player.removeAttribute("controls")
        },
        showControls: function() {
            this._player.setAttribute("controls", !0)
        },
        switchFullScreen: function() {
            this._oplayer.controls.fullscreenPanel.switchFullScreen({})
        }
    }; (function() {
        this.FX = function(d, c, e, f, m, l) {
            this.el = b.get(d);
            this.attributes = c;
            this.duration = e || 0.7;
            this.transition = f && f in FX.transitions ? f: "easeInOut";
            this.callback = m ||
            function() {};
            this.ctx = l || window;
            this.units = {};
            this.frame = {};
            this.endAttr = {};
            this.startAttr = {}
        };
        this.FX.transitions = {
            linear: function(b, d, c, e) {
                return c * b / e + d
            },
            easeIn: function(b, d, c, e) {
                return - c * Math.cos(b / e * (Math.PI / 2)) + c + d
            },
            easeOut: function(b, d, c, e) {
                return c * Math.sin(b / e * (Math.PI / 2)) + d
            },
            easeInOut: function(b, d, c, e) {
                return - c / 2 * (Math.cos(Math.PI * b / e) - 1) + d
            }
        };
        this.FX.prototype = {
            start: function() {
                var b = this;
                this.getAttributes();
                this.duration *= 1E3;
                this.time = (new Date).getTime();
                this.animating = !0;
                this.timer = setInterval(function() {
                    var d = (new Date).getTime();
                    d < b.time + b.duration ? (b.elapsed = d - b.time, b.setCurrentFrame()) : (b.frame = b.endAttr, b.complete());
                    b.setAttributes()
                },
                10)
            },
            ease: function(b, d) {
                return FX.transitions[this.transition](this.elapsed, b, d - b, this.duration)
            },
            complete: function() {
                clearInterval(this.timer);
                this.timer = null;
                this.animating = !1;
                this.callback.call(this.ctx)
            },
            setCurrentFrame: function() {
                for (var b in this.startAttr) if (this.startAttr[b] instanceof Array) {
                    this.frame[b] = [];
                    for (var d = 0; d < this.startAttr[b].length; d++) this.frame[b][d] = this.ease(this.startAttr[b][d], this.endAttr[b][d])
                } else this.frame[b] = this.ease(this.startAttr[b], this.endAttr[b])
            },
            getAttributes: function() {
                for (var d in this.attributes) switch (d) {
                case "color":
                case "borderColor":
                case "border-color":
                case "backgroundColor":
                case "background-color":
                    this.startAttr[d] = c(this.attributes[d].from || b.getStyle(this.el, d));
                    this.endAttr[d] = c(this.attributes[d].to);
                    break;
                case "scrollTop":
                case "scrollLeft":
                    var f = this.el == document.body ? document.documentElement || document.body: this.el;
                    this.startAttr[d] = this.attributes[d].from || f[d];
                    this.endAttr[d] = this.attributes[d].to;
                    break;
                default:
                    var h = this.attributes[d].to,
                    j = this.attributes[d].units || "px";
                    this.attributes[d].from ? f = this.attributes[d].from: (f = parseFloat(b.getStyle(this.el, d)) || 0, "px" != j && document.defaultView && (b.setStyle(this.el, d, (h || 1) + j), f *= (h || 1) / parseFloat(b.getStyle(this.el, d)), b.setStyle(this.el, d, f + j)));
                    this.units[d] = j;
                    this.endAttr[d] = h;
                    this.startAttr[d] = f
                }
            },
            setAttributes: function() {
                for (var d in this.frame) switch (d) {
                case "opacity":
                    b.setStyle(this.el, d, this.frame[d]);
                    break;
                case "scrollLeft":
                case "scrollTop":
                    (this.el == document.body ? document.documentElement || document.body: this.el)[d] = this.frame[d];
                    break;
                case "color":
                case "borderColor":
                case "border-color":
                case "backgroundColor":
                case "background-color":
                    b.setStyle(this.el, d, "rgb(" + Math.floor(this.frame[d][0]) + "," + Math.floor(this.frame[d][1]) + "," + Math.floor(this.frame[d][2]) + ")");
                    break;
                default:
                    b.setStyle(this.el, d, this.frame[d] + this.units[d])
                }
            }
        };
        var b = {
            get: function(b) {
                return "string" == typeof b ? document.getElementById(b) : b
            },
            getStyle: function(b, c) {
                var c = d(c),
                e = document.defaultView;
                return e && e.getComputedStyle ? e.getComputedStyle(b, "")[c] || null: "opacity" == c ? (e = b.filters("alpha").opacity, isNaN(e) ? 1 : e ? e / 100 : 0) : b.currentStyle[c] || null
            },
            setStyle: function(b, c, e) {
                "opacity" == c ? (b.style.filter = "alpha(opacity=" + 100 * e + ")", b.style.opacity = e) : (c = d(c), b.style[c] = e)
            }
        },
        d = function() {
            var b = {};
            return function(d) {
                if (b[d]) return b[d];
                var c = d.split("-"),
                e = c[0];
                if (1 < c.length) for (var f = 1,
                l = c.length; f < l; f++) e += c[f].charAt(0).toUpperCase() + c[f].substring(1);
                return b[d] = e
            }
        } (),
        c = function() {
            var b = /^#?(\w{2})(\w{2})(\w{2})$/,
            d = /^#?(\w{1})(\w{1})(\w{1})$/,
            c = /^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/;
            return function(e) {
                var f = e.match(b);
                if (f && 4 == f.length) return [parseInt(f[1], 16), parseInt(f[2], 16), parseInt(f[3], 16)];
                if ((f = e.match(c)) && 4 == f.length) return [parseInt(f[1], 10), parseInt(f[2], 10), parseInt(f[3], 10)];
                if ((f = e.match(d)) && 4 == f.length) return [parseInt(f[1] + f[1], 16), parseInt(f[2] + f[2], 16), parseInt(f[3] + f[3], 16)]
            }
        } ()
    })();
    FX.transitions.quadIn = function(b, d, c, g) {
        return c * (b /= g) * b + d
    };
    FX.transitions.quadOut = function(b, d, c, g) {
        return - c * (b /= g) * (b - 2) + d
    };
    FX.transitions.quadInOut = function(b, d, c, g) {
        return 1 > (b /= g / 2) ? c / 2 * b * b + d: -c / 2 * (--b * (b - 2) - 1) + d
    };
    FX.transitions.cubicIn = function(b, d, c, g) {
        return c * (b /= g) * b * b + d
    };
    FX.transitions.cubicOut = function(b, d, c, g) {
        return c * ((b = b / g - 1) * b * b + 1) + d
    };
    FX.transitions.cubicInOut = function(b, d, c, g) {
        return 1 > (b /= g / 2) ? c / 2 * b * b * b + d: c / 2 * ((b -= 2) * b * b + 2) + d
    };
    FX.transitions.quartIn = function(b, d, c, g) {
        return c * (b /= g) * b * b * b + d
    };
    FX.transitions.quartOut = function(b, d, c, g) {
        return - c * ((b = b / g - 1) * b * b * b - 1) + d
    };
    FX.transitions.quartInOut = function(b, d, c, g) {
        return 1 > (b /= g / 2) ? c / 2 * b * b * b * b + d: -c / 2 * ((b -= 2) * b * b * b - 2) + d
    };
    FX.transitions.quintIn = function(b, d, c, g) {
        return c * (b /= g) * b * b * b * b + d
    };
    FX.transitions.quintOut = function(b, d, c, g) {
        return c * ((b = b / g - 1) * b * b * b * b + 1) + d
    };
    FX.transitions.quintInOut = function(b, d, c, g) {
        return 1 > (b /= g / 2) ? c / 2 * b * b * b * b * b + d: c / 2 * ((b -= 2) * b * b * b * b + 2) + d
    };
    FX.transitions.expoIn = function(b, d, c, g) {
        return 0 == b ? d: c * Math.pow(2, 10 * (b / g - 1)) + d - 0.001 * c
    };
    FX.transitions.expoOut = function(b, d, c, g) {
        return b == g ? d + c: 1.001 * c * ( - Math.pow(2, -10 * b / g) + 1) + d
    };
    FX.transitions.expoInOut = function(b, d, c, g) {
        return 0 == b ? d: b == g ? d + c: 1 > (b /= g / 2) ? c / 2 * Math.pow(2, 10 * (b - 1)) + d - 5.0E-4 * c: 1.0005 * (c / 2) * ( - Math.pow(2, -10 * --b) + 2) + d
    };
    FX.transitions.circIn = function(b, c, e, g) {
        return - e * (Math.sqrt(1 - (b /= g) * b) - 1) + c
    };
    FX.transitions.circOut = function(b, c, e, g) {
        return e * Math.sqrt(1 - (b = b / g - 1) * b) + c
    };
    FX.transitions.circInOut = function(b, c, e, g) {
        return 1 > (b /= g / 2) ? -e / 2 * (Math.sqrt(1 - b * b) - 1) + c: e / 2 * (Math.sqrt(1 - (b -= 2) * b) + 1) + c
    };
    FX.transitions.backIn = function(b, c, e, g, f) {
        f = f || 1.70158;
        return e * (b /= g) * b * ((f + 1) * b - f) + c
    };
    FX.transitions.backOut = function(b, c, e, g, f) {
        f = f || 1.70158;
        return e * ((b = b / g - 1) * b * ((f + 1) * b + f) + 1) + c
    };
    FX.transitions.backBoth = function(b, c, e, g, f) {
        f = f || 1.70158;
        return 1 > (b /= g / 2) ? e / 2 * b * b * (((f *= 1.525) + 1) * b - f) + c: e / 2 * ((b -= 2) * b * (((f *= 1.525) + 1) * b + f) + 2) + c
    };
    FX.transitions.elasticIn = function(b, c, e, g, f, h) {
        if (0 == b) return c;
        if (1 == (b /= g)) return c + e;
        h || (h = 0.3 * g); ! f || f < Math.abs(e) ? (f = e, e = h / 4) : e = h / (2 * Math.PI) * Math.asin(e / f);
        return - (f * Math.pow(2, 10 * (b -= 1)) * Math.sin((b * g - e) * 2 * Math.PI / h)) + c
    };
    FX.transitions.elasticOut = function(b, c, e, g, f, h) {
        if (0 == b) return c;
        if (1 == (b /= g)) return c + e;
        h || (h = 0.3 * g);
        if (!f || f < Math.abs(e)) var f = e,
        j = h / 4;
        else j = h / (2 * Math.PI) * Math.asin(e / f);
        return f * Math.pow(2, -10 * b) * Math.sin((b * g - j) * 2 * Math.PI / h) + e + c
    };
    FX.transitions.elasticBoth = function(b, c, e, g, f, h) {
        if (0 == b) return c;
        if (2 == (b /= g / 2)) return c + e;
        h || (h = g * 0.3 * 1.5);
        if (!f || f < Math.abs(e)) var f = e,
        j = h / 4;
        else j = h / (2 * Math.PI) * Math.asin(e / f);
        return 1 > b ? -0.5 * f * Math.pow(2, 10 * (b -= 1)) * Math.sin((b * g - j) * 2 * Math.PI / h) + c: 0.5 * f * Math.pow(2, -10 * (b -= 1)) * Math.sin((b * g - j) * 2 * Math.PI / h) + e + c
    };
    FX.transitions.backIn = function(b, c, e, g, f) {
        "undefined" == typeof f && (f = 1.70158);
        return e * (b /= g) * b * ((f + 1) * b - f) + c
    };
    FX.transitions.backOut = function(b, c, e, g, f) {
        "undefined" == typeof f && (f = 1.70158);
        return e * ((b = b / g - 1) * b * ((f + 1) * b + f) + 1) + c
    };
    FX.transitions.backBoth = function(b, c, e, g, f) {
        "undefined" == typeof f && (f = 1.70158);
        return 1 > (b /= g / 2) ? e / 2 * b * b * (((f *= 1.525) + 1) * b - f) + c: e / 2 * ((b -= 2) * b * (((f *= 1.525) + 1) * b + f) + 2) + c
    };
    FX.transitions.bounceIn = function(b, c, e, g) {
        return e - FX.transitions.bounceOut(g - b, 0, e, g) + c
    };
    FX.transitions.bounceOut = function(b, c, e, g) {
        return (b /= g) < 1 / 2.75 ? e * 7.5625 * b * b + c: b < 2 / 2.75 ? e * (7.5625 * (b -= 1.5 / 2.75) * b + 0.75) + c: b < 2.5 / 2.75 ? e * (7.5625 * (b -= 2.25 / 2.75) * b + 0.9375) + c: e * (7.5625 * (b -= 2.625 / 2.75) * b + 0.984375) + c
    };
    FX.transitions.bounceBoth = function(b, c, e, g) {
        return b < g / 2 ? 0.5 * FX.transitions.bounceIn(2 * b, 0, e, g) + c: 0.5 * FX.transitions.bounceOut(2 * b - g, 0, e, g) + 0.5 * e + c
    };
    var Da = function(b) {
        b = parseInt(b);
        return Math.min(Math.max(b, 0), c.videoInfo.totalTime)
    },
    u = function(b) {
        var c = [],
        e;
        for (e in b) c.push(e + ":" + b[e]);
        return "{" + c.join(",") + "}"
    },
    q = function(b) {
        var c = [],
        e;
        for (e in b) c.push(e + "=" + b[e]);
        return c.join("&")
    },
    J = function(b) {
        if (!b) return "";
        var b = b.toString(),
        c,
        e,
        g,
        f,
        h,
        j;
        g = b.length;
        e = 0;
        for (c = ""; e < g;) {
            f = b.charCodeAt(e++) & 255;
            if (e == g) {
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(f >> 2);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 3) << 4);
                c += "==";
                break
            }
            h = b.charCodeAt(e++);
            if (e == g) {
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(f >> 2);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 3) << 4 | (h & 240) >> 4);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((h & 15) << 2);
                c += "=";
                break
            }
            j = b.charCodeAt(e++);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(f >> 2);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 3) << 4 | (h & 240) >> 4);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((h & 15) << 2 | (j & 192) >> 6);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(j & 63)
        }
        return c
    },
    K = {
        "-100": "\u8be5\u89c6\u9891\u6b63\u5728\u8f6c\u7801\u4e2d... , \u8bf7\u7a0d\u5019",
        "-101": "\u8be5\u89c6\u9891\u6b63\u5728\u5ba1\u6838\u4e2d... , \u8bf7\u7a0d\u5019",
        "-102": "\u8be5\u89c6\u9891\u5df2\u88ab\u5c4f\u853d",
        "-103": "\u8be5\u89c6\u9891\u8f6c\u7801\u5931\u8d25",
        "-201": "\u8be5\u89c6\u9891\u88ab\u8bbe\u4e3a\u79c1\u5bc6",
        "-202": "\u8be5\u89c6\u9891\u5df2\u7ecf\u52a0\u5bc6",
        "-203": "\u5bf9\u4e0d\u8d77\uff0c\u60a8\u8f93\u5165\u7684\u5bc6\u7801\u9519\u8bef\uff0c\u8bf7\u91cd\u65b0\u8f93\u5165",
        "-204": "\u7c89\u4e1d\u89c2\u770b\u89c6\u9891",
        "-301": "",
        "-302": "\u4ed8\u8d39\u89c6\u9891\u8d85\u8fc7\u89c2\u770b\u4e0a\u9650\u6b21\u6570",
        "-303": "\u4ed8\u8d39\u89c6\u9891\u4e0b\u7ebf",
        "-306": "\u8d26\u53f7\u5206\u4eab\u4e0d\u5408\u6cd5, IP\u4e0a\u9650",
        "-307": "\u4ed8\u8d39\u89c6\u9891, \u672a\u767b\u5f55",
        "-401": "\u96c6\u56e2\u64ad\u63a7\u7cfb\u7edf\u9650\u5236",
        "-402": "\u7528\u6237\u6ca1\u6709\u6743\u9650\u89c2\u770b(\u9632\u76d7\u94fenonce)",
        "-501": "\u670d\u52a1\u5668\u53d1\u751f\u9519\u8bef",
        "-601": "\u53c2\u6570\u9519\u8bef"
    },
    U = function(b, d) {
        this.player = b;
        this._handle = {};
        this._feedback = c.get(".x-feedback");
        this._message = this._feedback.getElementsByClassName("x-message")[0];
        this._messagetxt = this._message.getElementsByClassName("x-message-txt")[0];
        this._messagebtn = this._message.getElementsByClassName("x-message-btn")[0];
        this._errorcode = this._error = null;
        this.init(d);
        this.bindEvent()
    };
    U.prototype = {
        init: function(b) {
            if (b && b.data && b.data && b.data.error) {
                c.hide(c.get(".x-video-button"));
                c.hide(c.get(".x-console"));
                this._vid = b.data.id;
                this._title = b.data.video.title;
                this._userid = b.data.video.userid;
                this._error = b.data.error;
                this._errorcode = parseInt(b.data.error.code);
                switch (this._errorcode) {
                case - 100 : this.setMessage(K["-100"]);
                    break;
                case - 101 : this.setMessage(K["-101"]);
                    break;
                case - 102 : this.setMessage(K["-102"]);
                    this.setButton("\u641c\u7d22", this.search);
                    break;
                case - 103 : this.setMessage(K["-103"]);
                    this.bind_feedback = c.bindAsEventListener(this, this.feedback);
                    this.setButton("\u5728\u7ebf\u53cd\u9988", this.bind_feedback);
                    break;
                case - 201 : this.setMessage(K["-201"]);
                    this.bind_contact = c.bindAsEventListener(this, this.contactOwner);
                    this.setButton("\u8054\u7cfb\u4e0a\u4f20\u8005", this.bind_contact);
                    break;
                case - 202 : this._messagetxt.innerHTML = "<input type=password placeholder=\u8f93\u5165\u5bc6\u7801\u89c2\u770b\u89c6\u9891 class=x-message-input>";
                    this.bind_inputpassword = c.bindAsEventListener(this, this.inputPassword);
                    this.setButton("\u786e\u5b9a", this.bind_inputpassword);
                    break;
                case - 203 : this._messagetxt.innerHTML = '<input type=password placeholder="\u5bf9\u4e0d\u8d77,\u60a8\u8f93\u5165\u7684\u5bc6\u7801\u9519\u8bef,\u8bf7\u91cd\u65b0\u8f93\u5165" class=x-message-input>';
                    this.bind_inputpassword = c.bindAsEventListener(this, this.inputPassword);
                    this.setButton("\u786e\u5b9a", this.bind_inputpassword);
                    break;
                case - 301 : break;
                case - 306 : this._messagetxt.innerHTML = '<a style="color:#3399e0;text-decoration:underline;position:relative;top:3px;" href="' + b.data.error.link + '" target="_blank">' + b.data.error.note + "</a>";
                    break;
                default:
                    this.setMessage(b.data.error.note)
                }
                this.show();
                this.showMessage()
            }
        },
        bindEvent: function() {},
        show: function() {
            c.show(this._feedback)
        },
        hide: function() {
            c.hide(this._feedback)
        },
        showMessage: function() {
            c.show(this._message)
        },
        hideMessage: function() {
            c.hide(this._message)
        },
        setMessage: function(b) {
            this._messagetxt.innerHTML = "<p>" + b + "</p>"
        },
        setButton: function(b, d) {
            this._messagebtn.innerHTML = "<button type=button class=x-btn>" + b + "</button>";
            var e = this._message.getElementsByClassName("x-btn")[0];
            c.addEventHandler(e, "click", d)
        },
        search: function() {
            window.location.href = "http://www.soku.com/search_video/q_" + this._title
        },
        feedback: function() {
            window.location.href = "http://www.youku.com/service/feed/subtype/4/"
        },
        contactOwner: function() {
            window.location.href = "http://i.youku.com/u/id_" + this._userid
        },
        onPasswordConfirm: function() {},
        inputPassword: function() {
            var b = this._messagetxt.getElementsByClassName("x-message-input")[0],
            d = b.value;
            if (null == d || 0 == d.replace(/\s/g, "").length) b.value = "",
            b.placeholder = "\u5bc6\u7801\u4e3a\u7a7a\uff0c\u8bf7\u91cd\u65b0\u8f93\u5165";
            else {
                var e = this.player;
                c.password = d;
                l.start(this._vid, d, c.config.content,
                function(b, f) {
                    c.hide(c.get(".x-feedback"));
                    c.password = d;
                    c.show(c.get(".x-video-button"));
                    c.hide(c.get(".x-message"));
                    e.startPlay(b, f)
                })
            }
        }
    };
    var ia = function(b) {
        this._handler = {};
        this.player = b;
        this._fullflag = null;
        this.init();
        this._fullscreen = c.get(".x-fullscreen");
        this._btn = this._fullscreen.getElementsByTagName("button")[0];
        this._btnb = this._btn.getElementsByTagName("b")[0];
        this.bindEvent()
    };
    ia.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        init: function() {},
        bindEvent: function() {
            this.bind_switch = c.bindAsEventListener(this, this.switchFullScreen);
            c.addEventHandler(this._fullscreen, "click", this.bind_switch, !0)
        },
        removeEvent: function() {
            c.removeEventHandler(this._fullscreen, "click", this.bind_switch, !0)
        },
        zoomStatus: function() {
            return this._btnb.className
        },
        fullFlag: function() {
            if (null !== this._fullflag) return this._fullflag;
            var b = this.player.video.fullscreenchange;
            return this._fullflag = "undefined" != typeof b ? b: !1
        },
        switchFullScreen: function(b) {
            var d = b.method || "c",
            e = this._btnb.className;
            c.config.events && c.config.events.onSwitchFullScreen ? ( - 1 === e.indexOf("in") ? (this._fullflag = !1, this._btnb.className = e.replace(/out/g, "in"), this.player.controls.hideShowListBtn(), this.player._reporter.sendUserActionReport("xexfs", d), this.player.adjustVideoRatio(1), this.dispatch({
                type: "exitfullscreen"
            })) : (this._fullflag = !0, this._btnb.className = e.replace(/in/g, "out"), this.player.controls.showShowListBtn(), this.player._reporter.sendUserActionReport("xenfs", d), this.player.adjustVideoRatio(), this.dispatch({
                type: "enterfullscreen"
            })), d = c.config.events.onSwitchFullScreen, d(b, e)) : (b = document.getElementById("x-player"), -1 === e.indexOf("in") ? (this.player._reporter.sendUserActionReport("xexfs", d), document.webkitCancelFullScreen && (this._btnb.className = e.replace(/out/g, "in"), this._fullflag = !1, document.webkitCancelFullScreen())) : (this.player._reporter.sendUserActionReport("xenfs", d), b.webkitRequestFullScreen ? (this._btnb.className = e.replace(/in/g, "out"), this._fullflag = !0, b.webkitRequestFullScreen()) : this.player.video.webkitSupportsFullscreen && 1 <= this.player.video.readyState && this.player.video.webkitEnterFullscreen()))
        }
    };
    var ja = function(b, d) {
        this.handler = {};
        this.player = b;
        this.information = c.get(".x-video-info");
        this.title = this.information.getElementsByClassName("x-title")[0];
        this.videoState = this.information.getElementsByClassName("x-video-state")[0];
        c.hide(this.videoState);
        this.init(d)
    };
    ja.prototype = {
        init: function(b) {
            this.title.innerHTML = b.data.show && b.data.show.title ? b.data.show.title.substr(0, 20) : b.data.video.title.substr(0, 20);
            if (b.data.trial || b.data.error) if ("episodes" == c.v.data.trial.type) this.show();
            else return;
            this.videoState.innerHTML = "<span>\u65f6\u957f: " + c.getTime(parseInt(b.data.video.seconds)) + "</span>";
            this.show()
        },
        show: function() {
            if (c.v.data.trial) if ("episodes" == c.v.data.trial.type) c.show(this.information);
            else return;
            c.show(this.information)
        },
        hide: function() {
            c.hide(this.information)
        },
        bindEvent: function() {}
    };
    var ka = function(b) {
        this.player = b;
        this._tip = c.get(".x-prompt");
        this.init()
    };
    ka.prototype = {
        init: function() {
            this._tip.innerHTML = '<div class=x-prompt-mode><div class=x-prompt-time></div><div class=x-prompt-forward>\u5feb\u8fdb</div><div class=x-prompt-back>\u5feb\u9000</div><div class=x-mask></div></div><div class=x-prompt-status style="display:none"><div class=x-prompt-txt></div><div class=x-mask></div></div>';
            this._mode = this._tip.getElementsByClassName("x-prompt-mode")[0];
            this._time = this._tip.getElementsByClassName("x-prompt-time")[0];
            this._back = this._tip.getElementsByClassName("x-prompt-back")[0];
            this._forward = this._tip.getElementsByClassName("x-prompt-forward")[0];
            this._status = this._tip.getElementsByClassName("x-prompt-status")[0];
            this._statusTxt = this._tip.getElementsByClassName("x-prompt-txt")[0]
        },
        setProgress_: function(b) { ! 0 != this._progressFlag && (this._time.innerHTML = c.getTime(parseInt(b)))
        },
        setStatus: function(b) {
            this._statusTxt.innerHTML = b;
            this.showStatus()
        },
        hideStatus: function() {
            c.hide(this._status);
            c.hide(this._tip)
        },
        showStatus: function() {
            c.hide(this._mode);
            c.show(this._status);
            c.show(this._tip)
        },
        setTip: function(b, d) {
            this._progressFlag = !0;
            this._time.innerHTML = c.getTime(Da(b + d));
            0 >= d ? (c.show(this._back), c.hide(this._forward)) : (c.show(this._forward), c.hide(this._back));
            var e = this;
            setTimeout(function() {
                e._progressFlag = false
            },
            1E3)
        },
        isVisible: function() {
            return "none" != this._tip.style.display
        },
        hide: function() {
            c.hide(this._tip)
        },
        show: function() {
            c.show(this._mode);
            c.hide(this._status);
            c.show(this._tip)
        },
        autoHide: function(b) {
            var c = this;
            setTimeout(function() {
                c.hide()
            },
            b || 1E3)
        }
    };
    var la = function(b, d) {
        var e = !0;
        this._handler = {};
        if (c.isWeixin) c.get(".x-localization").style.display = "none";
        else if (!d || !d.data || !d.data || !d.data.dvd || !d.data.dvd.audiolang) c.get(".x-localization").style.display = "none";
        else {
            if (c.videoInfo._videoSegsDic) {
                var g = c.videoInfo._videoSegsDic.streams,
                f = !1,
                h;
                for (h in g) {
                    e = "";
                    for (k in g[h]) e += k + ","; (e = -1 < e.indexOf("3gphd") || -1 < e.indexOf("mp4") ? !1 : !0) && (f = !0)
                }
                if (e && f) {
                    c.get(".x-localization").style.display = "none";
                    return
                }
            }
            this.player = b;
            this._language = c.get(".x-localization");
            this.init(d);
            this.bindEvent();
            this._button = this._language.getElementsByTagName("button")[0];
            this._panel = this._language.getElementsByTagName("div")[0];
            this._nodes = this._language.getElementsByTagName("li")
        }
    };
    la.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        init: function(b) {
            for (var b = b.data,
            c = b.dvd.audiolang,
            e = ["<button class=x-control-btn>", "", "</button>"], g = ["<div class=x-panel><ul>", "", "</ul><div class=x-mask></div>", "</div>"], f = [], h = 0; h < c.length; h++) {
                var j = "",
                j = j + ("<li data-vid=" + c[h].vid),
                j = j + (" data-language=" + c[h].lang),
                j = j + (" data-language-code=" + c[h].langcode);
                c[h].vid == b.video.encodeid ? (e[1] = c[h].lang, j += " class=selected>") : j += ">";
                j += c[h].lang + "</li>";
                f[h] = j
            }
            g[1] = f.join("");
            this._language.innerHTML = e.join("") + g.join("")
        },
        bindEvent: function() {
            var b = this._language.getElementsByTagName("li");
            if (0 != b.length) {
                this.bind_toggle = c.bindAsEventListener(this, this.toggleLanguagePanel);
                c.addEventHandler(this._language, "click", this.bind_toggle);
                for (var d = 0; d < b.length; d++) c.addEventHandler(b[d], "click", c.bindAsEventListener(this, this.switchLanguage))
            }
        },
        removeEvent: function() {
            null != this._language && c.removeEventHandler(this._language, "click", this.bind_toggle)
        },
        hide: function(b) {
            if (this._language) {
                var c = this._panel;
                this._language.className = this._language.className.replace(/[\s]*pressed/g, "");
                c.style.display = "none";
                b || this.dispatch({
                    type: "settinghide"
                })
            }
        },
        toggleLanguagePanel: function(b) {
            var c = this._panel; - 1 === this._language.className.indexOf("pressed") ? (this._language.className += " pressed", c.style.display = "block", this.dispatch({
                type: "settingshow"
            }), this.player._reporter.sendUserActionReport("xcl", "c")) : (this.hide(), this.player._reporter.sendUserActionReport("xhl", "c"));
            this.dispatch(b)
        },
        switchLanguage: function(b) {
            this.player._reporter.sendUserActionReport("xsl", "c");
            b.stopPropagation();
            var b = b.target,
            d = null;
            b.getAttribute ? (d = b.getAttribute("data-vid"), b.getAttribute("data-language"), b = b.getAttribute("data-language-code")) : (d = b.parentNode.getAttribute("data-vid"), b.parentNode.getAttribute("data-language"), b = b.parentNode.getAttribute("data-language-code"));
            for (var e = this._nodes,
            g = 0; g < e.length; g++) if (e[g].getAttribute("data-vid") == d) {
                if ( - 1 !== e[g].className.indexOf("selected")) {
                    this.toggleLanguagePanel();
                    return
                }
                e[g].innerHTML = e[g].getAttribute("data-language");
                e[g].className += " selected";
                this._button.innerHTML = e[g].getAttribute("data-language")
            } else e[g].innerHTML = e[g].getAttribute("data-language"),
            e[g].className = e[g].className.replace(/[\s]*selected/g, "");
            this.toggleLanguagePanel();
            this.dispatch({
                type: "settingdone"
            });
            var f = this.player,
            h = this.player.currentTime;
            console.log("switchLanguage vid = " + d);
            c.config.nextAutoPlay = 1;
            if (null != c.videoInfo._videoSegsDic && null != c.videoInfo._videoSegsDic.streams[b]) {
                if ("m3u8" == c.config.content) c.defaultLanguage = b,
                f.video.src = c.m3u8src_v2(d, c.defaultVideoType);
                else {
                    d = c.videoInfo._videoSegsDic.streams[b];
                    if (d[c.defaultVideoType]) c.defaultLanguage = b;
                    else {
                        e = ["3gphd", "mp4"];
                        for (g = 0; g < e.length; g++) if (d[e[g]]) {
                            c.defaultVideoType = e[g];
                            c.defaultLanguage = b;
                            break
                        }
                    }
                    f.video.src = c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][0].src
                }
                f.video.load();
                f.video.play()
            }
            var j = 0;
            f.video.addEventListener("canplay",
            function() {
                if (j !== 1) {
                    j = 1;
                    f.seek(h)
                }
            })
        }
    };
    var n = {
        setItem: function(b, c) {
            try {
                window.localStorage.setItem(b, c)
            } catch(e) {}
        },
        appendItem: function(b, c) {
            "phase" == b && !this.phaseTag && (this.phaseTag = !0, n.removeItem("phase"));
            try {
                var e = n.getItem(b);
                null !== e && (c = e + "-" + c);
                window.localStorage.setItem(b, c)
            } catch(g) {}
        },
        getItem: function(b) {
            try {
                return window.localStorage.getItem(b)
            } catch(c) {
                return null
            }
        },
        removeItem: function(b) {
            try {
                window.localStorage.removeItem(b)
            } catch(c) {}
        }
    },
    ma = function(b) {
        this.player = b;
        this._progress = c.get(".x-progress-mini");
        this._track = this._progress.getElementsByClassName("x-progress-track-mini")[0];
        this._play = this._progress.getElementsByClassName("x-progress-play-mini")[0];
        this._load = this._progress.getElementsByClassName("x-progress-load-mini")[0];
        this._handler = {};
        this.bindEvent();
        this.resetProgress();
        this.hide()
    };
    ma.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        bindEvent: function() {},
        removeEvent: function() {},
        dispatch: function(b) {
            if (b && this._handler[b.type]) this._handler[b.type]()
        },
        setProgress: function(b, d) {
            var e = Math.min(b, c.videoInfo.totalTime);
            this.playTime = e;
            var g = e / c.videoInfo.totalTime;
            this._play.style.width = 100 * g + "%"; ! 0 !== d && (this.loadTime = e += Math.max(this.player.bufferedEnd() - b, 0), g = e / c.videoInfo.totalTime + 0.05, this._load.style.width = 100 * Math.min(Math.max(g, 0), 1) + "%")
        },
        resetProgress: function() {
            this._play.style.width = "0%";
            this._load.style.width = "0%"
        },
        show: function() {
            this._progress.style.display = "block"
        },
        hide: function() {
            this._progress.style.display = "none"
        }
    };
    var na = function(b, d) {
        this._handler = {};
        this._hasPayInfo = !1;
        this._payInfo = c.get(".x-pay");
        this._text = c.get(".x-pay-txt");
        this._title = this._text.getElementsByTagName("h1")[0];
        this._vip = this._text.getElementsByTagName("em")[0];
        this._tip = c.get(".x-pay-tips");
        this._button = c.get(".x-pay-btn");
        this._tryBtn = c.get("#x-try");
        this._payBtn = c.get("#x-pay");
        this.player = b;
        this.init(d)
    };
    na.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        bindEvent: function() {
            this.bind_try = c.bindAsEventListener(this, this.play);
            this.bind_pay = c.bindAsEventListener(this, this.pay);
            c.addEventHandler(this._tryBtn, "click", this.bind_try);
            c.addEventHandler(this._payBtn, "click", this.bind_pay)
        },
        removeEvent: function() {
            c.removeEventHandler(this._tryBtn, "click", this.bind_try);
            c.removeEventHandler(this._payBtn, "click", this.bind_pay)
        },
        init: function(b) {
            if (null == b.data.trial) debug.log("not pay");
            else if (! (b.data.trial && "episodes" == b.data.trial.type)) {
                this._hasPayInfo = !0;
                this._showid = b.data.show.id;
                this._type = b.data.show.pay_type;
                var c = b.data.video.title;
                12 < c.length && (c = c.substr(0, 12) + "...");
                this._tryDuration = parseInt(b.data.trial.time);
                this.player.tryDuration = this._tryDuration;
                debug.log("try = " + this._tryDuration);
                "vod" == this._type ? (this._title.innerHTML = c + "<em class=x-vip>\u4ed8\u8d39\u5f71\u7247</em>", this._payBtn.innerHTML = "\u7acb\u5373\u8d2d\u4e70") : (this._title.innerHTML = c + "<em class=x-vip>\u4ed8\u8d39\u5305\u6708\u5f71\u7247</em>", this._payBtn.innerHTML = "\u5f00\u901a\u4f1a\u5458");
                this.bindEvent();
                this.show();
                this.player._reporter.sendPayReport()
            }
        },
        play: function() {
            if ((f.isIPHONE || f.isIPOD) && null != c.v.data.trial) this.player.video.style.display = "block";
            0 === this.activeTime ? this.player.seek(0) : this.player.video.play();
            this.player._reporter.sendUserActionReport("xtry", "c")
        },
        pay: function() {
            this.player.video.pause();
            c.v.data.pay && c.v.data.pay.h5_caseurl && window.open(c.v.data.pay.h5_caseurl, "", "", !1);
            this.player._reporter.sendUserActionReport("xbuy", "c")
        },
        hide: function() {
            this._payInfo && (this._payInfo.style.display = "none")
        },
        show: function() { ! 1 != this._hasPayInfo && (this._payInfo.style.display = "block", 0 >= this._tryDuration && c.hide(this._tryBtn))
        },
        isBlock: function() {
            return "block" == this._payInfo.style.display
        },
        showTip: function() {
            this._hasPayInfo && (this._tip.innerHTML = "\u514d\u8d39\u8bd5\u770b\u5df2\u7ecf\u7ed3\u675f\uff0c\u4ed8\u8d39\u5373\u53ef\u89c2\u770b", this.show())
        },
        clearTip: function() {
            this._tip.innerHTML = ""
        },
        hasPayInfo: function() {
            return this._hasPayInfo
        },
        tryDuration: function() {
            return this._tryDuration
        }
    };
    var oa = function(b, c) {
        this._handler = {};
        this.player = b;
        this._videoInfo = c;
        this._isLimit = this._html5_disable = !1;
        this._limitMinute = 40;
        this._videoInfo.data.controller && !0 == this._videoInfo.data.controller.html5_disable && (this._html5_disable = this._isLimit = !0);
        this._limitTime = this._videoInfo.data.trial && "episodes" != this._videoInfo.data.trial.type ? this._videoInfo.data.trial.time: 60 * this._limitMinute;
        this._html5_disable && (this.player.tryDuration = this._limitTime);
        this._isCreated = !1;
        debug.log("videoInfo.controller.xplayer_disable:", this._isLimit);
        debug.log("videoInfo.controller.app_disable:", this._app_disable)
    };
    oa.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        create: function() {
            if (!this._isCreated) {
                debug.log("playLimit create");
                this.player.video.pause();
                this._isCreated = !0;
                var b = c.get("#x-player"); ! 1 != this._html5_disable && (c.v.data.trial && "episodes" != c.v.data.trial.type ? f.Log("http://hz.youku.com/red/click.php?tp=1&cp=4009227&cpp=1000752&url=") : (b.innerHTML = "<div class=x-app-guide><div class=x-app-guide-tips><p>\u672c\u9875\u9762\u63d0\u4f9b" + this._limitMinute + '\u5206\u949f\u9884\u89c8</p></div><div class=x-app-guide-action><button type=button class="x-btn x-btn-major">&nbsp;&nbsp;&nbsp;\u4f7f\u7528App\u89c2\u770b\u5b8c\u6574\u7248&nbsp;&nbsp;&nbsp;</button></div><div class=x-app-openapp></div></div>', this._content = c.get(".x-app-guide"), this._fullBtn = this._content.getElementsByClassName("x-btn")[0], this._openApp = this._content.getElementsByClassName("x-app-openapp")[0], this.bind_onFullClick = c.bindAsEventListener(this, this.onFullClick), c.addEventHandler(this._fullBtn, "click", this.bind_onFullClick), f.Log("http://hz.youku.com/red/click.php?tp=1&cp=4009227&cpp=1000752&url="), this._content.style.marginLeft = parseInt( - this._content.offsetWidth / 2) + "px", this._content.style.marginTop = parseInt( - this._content.offsetHeight / 2) + "px"))
            }
        },
        onFullClick: function() {
            debug.log("onFullClick");
            this._content.getElementsByClassName("x-app-guide-action")[0].innerHTML = '<button type=button class="x-btn x-btn-major">&nbsp;\u4e0b\u8f7d\u5b89\u88c5&nbsp;</button><button type=button class="x-btn">&nbsp;\u6211\u77e5\u9053\u4e86&nbsp;</button>';
            this._downloadBtn = this._content.getElementsByClassName("x-btn")[0];
            this._knowBtn = this._content.getElementsByClassName("x-btn")[1];
            this.bind_onDownload = c.bindAsEventListener(this, this.onDownloadClick);
            this.bind_onKnow = c.bindAsEventListener(this, this.onKnowClick);
            c.addEventHandler(this._downloadBtn, "click", this.bind_onDownload);
            c.addEventHandler(this._knowBtn, "click", this.bind_onKnow);
            f.Log("http://hz.youku.com/red/click.php?tp=1&cp=4009213&cpp=1000752&url=");
            this._content.getElementsByClassName("x-app-guide-tips")[0].innerHTML = "<p>\u770b\u5b8c\u6574\u7248\u9700\u5b89\u88c5\u6700\u65b0\u4f18\u9177app</p>";
            this._content.style.marginLeft = parseInt( - this._content.offsetWidth / 2) + "px";
            this._content.style.marginTop = parseInt( - this._content.offsetHeight / 2) + "px";
            this.openApp()
        },
        onDownloadClick: function() {
            f.Log("http://hz.youku.com/red/click.php?tp=1&cp=4009215&cpp=1000752&url=");
            f.isAndroid ? window.open("http://dl.m.cc.youku.com/android/phone/Youku_Android_xianbobofangqi.apk", "_blank") : window.open("http://hz.youku.com/red/click.php?tp=1&cp=4008066&cpp=1000687&url=http://m.youku.com/webapp/dl?app=youku&source=webqr", "_blank")
        },
        onKnowClick: function() {
            f.Log("http://hz.youku.com/red/click.php?tp=1&cp=4009216&cpp=1000752&url=");
            setTimeout(function() {
                window.location.reload()
            },
            500)
        },
        openApp: function() {
            var b = document.createElement("iframe");
            b.height = 0;
            b.width = 0;
            b.frameBorder = "no";
            b.src = "youku://play?vid=" + c.initConfig.vid;
            f.isIPAD && (b.src = "youkuhd://play?vid=" + c.initConfig.vid);
            document.getElementsByTagName("body")[0].appendChild(b)
        },
        isLimit: function() {
            return this._isLimit
        },
        limitTime: function() {
            return this._limitTime
        }
    };
    var F = {
        2 : "2\u500d",
        "1.5": "1.5\u500d",
        1 : "\u5e38\u901f",
        "0.8": "0.8\u500d"
    },
    pa = function(b, d) {
        this._handler = {}; ! c.isWeixin && f.isIPAD7 && (this.player = b, this.playRate = c.get(".x-playspeed"), this.init(d), this.bindEvent(), this.button = this.playRate.getElementsByTagName("button")[0], this.panel = this.playRate.getElementsByTagName("div")[0], this.nodes = this.playRate.getElementsByTagName("li"), c.show(this.playRate))
    };
    pa.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        init: function() {
            for (var b = ["<button class=x-control-btn>", "", "</button>"], c = ['<div class=x-panel style="display:none"><ul>', "", "</ul><div class=x-mask></div>", "</div>"], e = "", g = [], f = ["2", "1.5", "1", "0.8"], h = 0; h < f.length; h++) {
                var j = f[h],
                m = "",
                l = "";
                "1" == j && (m = "", b[1] = F[j], l = " class=selected");
                e += "<li data-vtype=" + j + l + ">" + m + F[j] + "</li>";
                g.push(F[j])
            }
            c[1] = e;
            this.playRate.innerHTML = b.join("") + c.join("")
        },
        bindEvent: function() {
            var b = this.playRate.getElementsByTagName("li");
            if (0 != b.length) {
                this.bind_toggle = c.bindAsEventListener(this, this.toggleRatePanel);
                c.addEventHandler(this.playRate, "click", this.bind_toggle);
                for (var d = 0; d < b.length; d++) c.addEventHandler(b[d], "click", c.bindAsEventListener(this, this.switchRate))
            }
        },
        removeEvent: function() {
            null != this.playRate && c.removeEventHandler(this.playRate, "click", this.bind_toggle)
        },
        hide: function(b) {
            if (this.playRate) {
                var c = this.panel;
                this.playRate.className = this.playRate.className.replace(/[\s]*pressed/g, "");
                c.style.display = "none";
                b || this.dispatch({
                    type: "settinghide"
                })
            }
        },
        toggleRatePanel: function(b) {
            var c = this.panel; - 1 === this.playRate.className.indexOf("pressed") ? (this.playRate.className += " pressed", c.style.display = "block", this.player._reporter.sendUserActionReport("xcra", "c"), this.dispatch({
                type: "settingshow"
            })) : (this.hide(), this.player._reporter.sendUserActionReport("xhra", "c"));
            this.dispatch(b)
        },
        switchRate: function(b) {
            b.stopPropagation();
            var c = b.target,
            b = null,
            b = c.getAttribute ? c.getAttribute("data-vtype") : c.parentNode.getAttribute("data-vtype");
            this.player._reporter.sendUserActionReport("xsra", "c", {
                rate: b
            });
            for (var c = this.button,
            e = this.nodes,
            g = 0; g < e.length; g++) if (e[g].getAttribute("data-vtype") == b) {
                if ( - 1 !== e[g].className.indexOf("selected")) {
                    this.toggleRatePanel();
                    return
                }
                e[g].innerHTML = F[b];
                e[g].className += " selected";
                c.innerHTML = F[b]
            } else {
                var f = e[g].getAttribute("data-vtype");
                e[g].innerHTML = F[f];
                e[g].className = e[g].className.replace(/selected/, "")
            }
            this.toggleRatePanel();
            this.dispatch({
                type: "settingdone"
            });
            this.player.video.pause();
            this.player.video.playbackRate = parseFloat(b);
            this.player.video.play()
        }
    };
    var qa = function(b) {
        this.player = b;
        this._progress = c.get(".x-progress");
        this._track = this._progress.getElementsByClassName("x-progress-track")[0];
        this._play = this._progress.getElementsByClassName("x-progress-play")[0];
        this._load = this._progress.getElementsByClassName("x-progress-load")[0];
        this._seek = this._progress.getElementsByClassName("x-progress-seek")[0];
        this._seekHandle = this._seek.getElementsByClassName("x-seek-handle")[0];
        this._handler = {};
        this.bindEvent()
    };
    qa.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        bindEvent: function() {
            this.bind_seek = c.bindAsEventListener(this, this.seek);
            this.bind_touchstart = c.bindAsEventListener(this, this.onTouchStart);
            c.addEventHandler(this._track, "click", this.bind_seek, !0);
            c.addEventHandler(this._seek, "touchstart", this.bind_touchstart)
        },
        removeEvent: function() {
            c.removeEventHandler(this._track, "click", this.bind_seek, !0);
            c.removeEventHandler(this._seek, "touchstart", this.bind_touchstart)
        },
        removeClickEvent: function() {
            c.removeEventHandler(this._track, "click", this.bind_seek, !0)
        },
        addClickEvent: function() {
            c.addEventHandler(this._track, "click", this.bind_seek, !0)
        },
        dispatch: function(b) {
            if (b && this._handler[b.type]) this._handler[b.type](b)
        },
        setProgress: function(b, d) {
            var e = Math.min(Math.max(b, 0), c.videoInfo.totalTime);
            this.playTime = e;
            var g = e / c.videoInfo.totalTime,
            f = this._track.offsetWidth,
            h = this._seek.offsetWidth;
            this._play.style.width = Math.min(100 * (g + h / f / 2), 100) + "%";
            this._seek.style.left = g * f > f - h ? f - h + "px": 100 * Math.min(Math.max(g, 0), 1) + "%";
            this.uCurrentTime.innerHTML = c.getTime(e); ! 0 !== d && (this.loadTime = e += Math.max(this.player.bufferedEnd() - b, 0), g = e / c.videoInfo.totalTime, this._load.style.width = 100 * Math.min(Math.max(g + 0.05, 0), 1) + "%")
        },
        resetProgress: function() {
            this._seek.style.left = this._seek.style.width;
            this._load.style.width = "0";
            this._play.style.width = "0"
        },
        getRate: function(b, d) {
            var e = 1,
            g = c.get(".x-fs-console");
            g && (e = parseFloat(c.getCurrentStyle(g).zoom));
            return b / (d * e)
        },
        seek: function(b) {
            var d = (new Date).getTime() - ra;
            if (b.srcElement == this._seek || d < sa) return debug.log(d + "," + sa),
            !1;
            this.player._reporter.sendUserActionReport("xcs", "c");
            d = b.offsetX || b.changedTouches[0].clientX - this._track.clientX;
            debug.log("x = " + d);
            var d = this.getRate(d, this._track.offsetWidth),
            e = d * c.videoInfo.totalTime;
            debug.log("progress bar time = " + e + "rate = " + d + "total = " + c.videoInfo.totalTime);
            this.setProgress(e, !0);
            this.dispatch({
                type: "progressend"
            });
            this.player.seek(e);
            this.dispatch(b)
        },
        handleX: function() {
            return 0
        },
        onTouchStart: function(b) {
            if (1 != b.targetTouches.length || this.isTouching) return ! 1;
            this.startX = b.targetTouches[0].clientX;
            b.preventDefault();
            this.isTouching = !0;
            this.startTime = this._currentTime = this.player.currentTime || 0;
            "m3u8" == c.config.content && (this._prepaused = this.player.video.paused, this.player.video.pause(), this.startTime = this.player.currentTime);
            if ("mp4" == c.config.content) {
                this.player.video.pause();
                this.startTime = this.player.video.currentTime;
                for (b = 0; b < s; b++) this.startTime += parseInt(c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][b].seconds)
            }
            this.bind_onTouchMove = c.bindAsEventListener(this, this.onTouchMove);
            this.bind_onTouchEnd = c.bindAsEventListener(this, this.onTouchEnd);
            c.addEventHandler(this._seek, "touchmove", this.bind_onTouchMove);
            c.addEventHandler(this._seek, "touchend", this.bind_onTouchEnd)
        },
        onTouchMove: function(b) {
            if (1 != b.targetTouches.length) return ! 1;
            b.preventDefault();
            b.stopPropagation();
            b = this.startTime + this.getRate(b.targetTouches[0].clientX - this.startX, this._track.offsetWidth) * c.videoInfo.totalTime;
            this.dispatch({
                type: "progressing",
                st: this._currentTime,
                dt: b - this._currentTime
            });
            this._currentTime = b;
            this.setProgress(Math.min(Math.max(this._currentTime, 0), c.videoInfo.totalTime), !0);
            return ! 1
        },
        onTouchEnd: function(b) {
            this.dispatch({
                type: "progressend"
            });
            this.isTouching = !1;
            if (1 < b.changedTouches.length) return ! 1;
            var d = {
                tb: parseInt(100 * this.startTime) / 100,
                to: parseInt(100 * this._currentTime) / 100
            };
            debug.log("tb=" + d.tb);
            this.player._reporter.sendUserActionReport("xds", "d", d);
            b.preventDefault();
            b.stopPropagation();
            c.removeEventHandler(this._seek, "touchmove", this.bind_onTouchMove);
            c.removeEventHandler(this._seek, "touchend", this.bind_onTouchEnd);
            b = Math.min(Math.max(this._currentTime, 0), c.videoInfo.totalTime - 5);
            this.player.controls.onPlay();
            var e = this.player;
            this.player.seek(b,
            function() {
                e.video.play()
            });
            return ! 1
        }
    };
    var ta = function(b, d) {
        this._handler = {};
        c.isWeixin && (c.get(".x-quality").style.display = "none");
        "m3u8" != c.config.content ? c.get(".x-quality").style.display = "none": !d || !d.data || !d.data.stream[0] || !d.data.stream[0].stream_type ? c.get(".x-quality").style.display = "none": (this.player = b, this._quality = c.get(".x-quality"), this.init(d), this.bindEvent(), this._button = this._quality.getElementsByTagName("button")[0], this._panel = this._quality.getElementsByTagName("div")[0], this._nodes = this._quality.getElementsByTagName("li"))
    };
    ta.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        init: function() {
            var b = c.videoInfo._videoSegsDic.typeArr,
            d = ["<button class=x-control-btn title=\u753b\u8d28\u8bbe\u7f6e>", "", "</button>"],
            e = ['<div class=x-panel style="display:none"><ul>', "", "</ul><div class=x-mask></div>", "</div>"],
            g = "",
            f = [],
            h;
            for (h in x) if ( - 1 !== b[c.defaultLanguage].indexOf(h) && -1 === f.indexOf(x[h])) {
                var j = "",
                m = "";
                h == c.defaultVideoType && (j = "", d[1] = x[h], m = " class=selected");
                g += "<li data-vtype=" + h + m + ">" + j + x[h] + "</li>";
                f.push(x[h])
            }
            "" == d[1] && (d[1] = f[0]);
            e[1] = g;
            this._quality.innerHTML = d.join("") + e.join("")
        },
        bindEvent: function() {
            var b = this._quality.getElementsByTagName("li");
            if (0 != b.length) {
                this.bind_toggle = c.bindAsEventListener(this, this.toggleQualityPanel);
                c.addEventHandler(this._quality, "click", this.bind_toggle);
                for (var d = 0; d < b.length; d++) c.addEventHandler(b[d], "click", c.bindAsEventListener(this, this.switchQuality))
            }
        },
        removeEvent: function() {
            null != this._quality && c.removeEventHandler(this._quality, "click", this.bind_toggle)
        },
        hide: function(b) {
            if (this._quality) {
                var c = this._panel;
                this._quality.className = this._quality.className.replace(/[\s]*pressed/g, "");
                c.style.display = "none";
                b || this.dispatch({
                    type: "settinghide"
                })
            }
        },
        toggleQualityPanel: function(b) {
            var c = this._panel; - 1 === this._quality.className.indexOf("pressed") ? (this._quality.className += " pressed", c.style.display = "block", this.player._reporter.sendUserActionReport("xcq", "c"), this.dispatch({
                type: "settingshow"
            })) : (this.hide(), this.player._reporter.sendUserActionReport("xhq", "c"));
            this.dispatch(b)
        },
        switchQuality: function(b) {
            this.player._reporter.sendUserActionReport("xsq", "c");
            b.stopPropagation();
            for (var d = b.target,
            b = null,
            b = d.getAttribute ? d.getAttribute("data-vtype") : d.parentNode.getAttribute("data-vtype"), d = this._button, e = this._nodes, g = 0; g < e.length; g++) if (e[g].getAttribute("data-vtype") == b) {
                if ( - 1 !== e[g].className.indexOf("selected")) {
                    this.toggleQualityPanel();
                    return
                }
                e[g].innerHTML = x[b];
                e[g].className += " selected";
                d.innerHTML = x[b];
                n.setItem("defaultVideoType", b);
                c.defaultVideoType = b
            } else {
                var f = e[g].getAttribute("data-vtype");
                e[g].innerHTML = x[f];
                e[g].className = e[g].className.replace(/selected/, "")
            }
            debug.log("q1");
            this.toggleQualityPanel();
            this.dispatch({
                type: "settingdone"
            });
            var h = this.player.currentTime,
            j = c.m3u8src_v2(c.v.data.id, b);
            c.unitedTag = null;
            this.player.video.src = j;
            var m = this,
            l = 0;
            this.player.video.addEventListener("canplay",
            function() {
                1 === l ? debug.log("XXXXXXXXXXXXXXXXXXXXX") : (l = 1, debug.log("q2 nsrc=" + j), m.player.seek(h), debug.log("q3"))
            });
            this.player.video.load();
            this.player.video.play()
        },
        switchQuality_: function(b) {
            b.stopPropagation();
            for (var b = b.target.dataset.vtype,
            c = this._button,
            e = this._nodes,
            g = 0; g < e.length; g++) if (e[g].dataset.vtype == b) {
                if ( - 1 !== e[g].className.indexOf("selected")) {
                    this.toggleQualityPanel();
                    return
                }
                e[g].innerHTML = x[b];
                e[g].className += " selected";
                c.innerHTML = x[b]
            } else e[g].innerHTML = x[e[g].dataset.vtype],
            e[g].className = e[g].className.replace(/selected/, "");
            debug.log("q1");
            this.toggleQualityPanel();
            var f = this.player.video.currentTime,
            h = this.player.video.src.replace(/type\/(flv|flvhd|mp4|hd2)/, "type/" + b);
            this.player.video.src = h;
            var j = this,
            m = 0;
            this.player.video.addEventListener("canplay",
            function() {
                1 === m ? debug.log("XXXXXXXXXXXXXXXXXXXXX") : (m = 1, debug.log("q2 nsrc=" + h), j.player.seek(f), debug.log("q3"))
            })
        }
    };
    var ua = function(b, d) {
        this._handler = {};
        this.player = b;
        this._panel = document.createElement("div");
        this._panel.className = "x-recommend";
        this.init(d);
        this.request(d);
        window.relatedpanel = this;
        c.get("#x-player").appendChild(this._panel);
        this._panel.style.display = "box";
        var e = {
            e: "xendcard"
        };
        e.device = f.isAndroid ? "adr": f.isIPAD ? "ipad": "oth";
        f.Log(f.uniplayerUrl + u(e))
    };
    ua.prototype = {
        bindDynamicEvent: function() {
            var b = this._listinner.getElementsByClassName("x-item");
            this.bind_itemclick = c.bindAsEventListener(this, this.onItemClick);
            for (var d = 0; d < b.length; d++) c.addEventHandler(b[d], "click", this.bind_itemclick, !0)
        },
        onItemClick: function(b) {
            b = b.currentTarget.getAttribute("data-i");
            "x" == b ? this.replay() : this.player._reporter.sendRecommendLog(this.getReportParam(b))
        },
        init: function() {
            this._panel.innerHTML = "<div class=x-pages></div>";
            this._listinner = this._panel.getElementsByClassName("x-pages")[0]
        },
        request: function(b) {
            var d, e = {};
            e.vid = b.data.id;
            e.uid = b.data.video.userid;
            b.data.show && b.data.show.id && (e.sid = b.data.show.id);
            e.cate = b.data.video.category_id;
            e.site = "1";
            e.module = "2";
            b = b.data.controller.play_mode;
            e.pg = "1";
            e.pg = {
                normal: 1,
                show: 3,
                folder: 4
            } [b];
            "interior" == c.config.winType ? e.apptype = 12 : (e.apptype = 12, e.pg = 1);
            e.pl = 36;
            for (d in c.initConfig.playlistconfig) e[d] = c.initConfig.playlistconfig[d];
            e.callback = "relatedpanel.parseResponse";
            d = "http://ykrec.youku.com/video/packed/list.json?" + q(e);
            A(d);
            this._apt = e.apptype;
            this._pg = e.pg;
            this._md = e.module
        },
        parseResponse: function(b) {
            this._info = b;
            this.buildPanel(this._info)
        },
        buildPanel: function(b) {
            var b = b.data,
            d = b.length;
            debug.log("realted len = " + d);
            var e = [];
            e.push('<ul class="x-item" data-i="x"><li class="x-item-img"><img src="http://player.youku.com/h5player/img/replay.png"></li></ul>');
            for (var g = Math.floor((this._panel.offsetWidth - 60 + 16) / 166) * Math.floor((this._panel.offsetHeight - 120 + 12) / 97), g = (g > d ? d: g) - 1, g = 0 > g ? 0 : g, d = 0; d < g; d++) {
                var f = b[d].picUrl,
                h = b[d].title.substr(0, 20),
                j = "http://v.youku.com/v_show/id_" + b[d].codeId + ".html?from=",
                m = "y7",
                m = "interior" == c.config.winType ? m + ".2-1-": m + ".7-1-",
                m = m + c.v.data.video.category_id,
                m = m + ".4",
                m = m + ("." + (d + 1) + "-1"),
                m = m + ("." + this._apt + "-" + this._pg + "-" + this._md + "-" + d),
                j = j + m;
                debug.log(j);
                "myoukucom" == c.initConfig.client_id && (j = "http://m.youku.com/smartphone/detail?vid=" + b[d].codeId);
                e.push('<ul class="x-item" data-i=' + d + '><li class="x-item-img"><img src=' + f + '></li><li class="x-item-info"><div class="x-item-title">' + h + '</div><div class="x-item-bg"></div></li><li class="x-item-url"><a href=' + j + ' target="_blank"></a></li><li class="x-item-loading"><div class="x-play-loading"></div></li></ul>')
            }
            this._listinner.innerHTML = e.join("");
            this.bindDynamicEvent();
            this.buildImgEvent()
        },
        getReportParam: function(b) {
            var d = {};
            d.pos = "" + b;
            d.sct = c.v.data.video.category_id;
            d.dct = this._info.data[b].dct;
            d.ord = this._info.ord;
            d.req_id = this._info.req_id;
            d.abver = this._info.ver;
            d.dma = this._info.data[b].dma;
            d.algInfo = this._info.data[b].algInfo;
            d.apt = this._apt;
            d.md = this._md;
            d.pg = this._pg;
            d.r = (new Date).getTime();
            d.vid = c.v.data.video.encodeid;
            d.uid = c.v.data.video.userid;
            1 == this._info.data[b].type ? d.dvid = this._info.data[b].id: d.dsid = this._info.data[b].id;
            d.sid = "";
            c.v.data.show && c.v.data.show.id && (d.sid = c.v.data.show.id);
            return d
        },
        buildImgEvent: function() {
            for (var b = this._listinner.getElementsByClassName("x-item-img"), d = 0; d < b.length; d++) c.addEventHandler(b[d], "error", c.bindAsEventListener(this, this.onLoadImgError)),
            c.addEventHandler(b[d], "abort", c.bindAsEventListener(this, this.onLoadImgError))
        },
        onLoadImgError: function(b) {
            debug.log("img error");
            b = b.target;
            c.addClass(b.parentNode.parentNode, "x-no-pic");
            b.src = "http://player.youku.com/h5player/img/no_pic.png"
        },
        replay: function(b) {
            this.player.controls.rePlay(b)
        },
        onResize: function() {
            var b = this;
            setTimeout(function() {
                b.buildPanel(b._info)
            },
            500)
        }
    };
    var va = function(b, d) {
        this._handler = {};
        this.player = b;
        this._showbtn = c.get(".x-playshow");
        this._showlist = c.get(".x-showlist");
        this.init(d);
        this._inner = this._showlist.getElementsByClassName("x-showlist-inner");
        this._bullet = this._showlist.getElementsByClassName("x-showlist-bullet");
        this.bindEvent()
    };
    va.prototype = {
        init: function(b) {
            this._showlist.innerHTML = '<div class=x-showlist-inner><div class=x-showlist-hd></div><div class=x-showlist-bd></div><div class=x-showlist-ft style="display:none"></div><div class=x-mask></div></div>';
            this._slhd = this._showlist.getElementsByClassName("x-showlist-hd")[0];
            this._slbd = this._showlist.getElementsByClassName("x-showlist-bd")[0];
            this._slft = this._showlist.getElementsByClassName("x-showlist-ft")[0];
            this._slhd.innerHTML = "<label>\u9009\u96c6</label><div class=x-showlist-close></div>";
            this._closeHandle = this._slhd.getElementsByClassName("x-showlist-close")[0];
            if (b.data.videos) {
                for (var d = b.data.videos.list,
                e = ["<ul class=x-showlist-bullet>", "", "</ul>"], g = [], f = 0; f < d.length; f++) {
                    var h = d[f],
                    j = "http://v.youku.com/v_show/id_" + h.encodevid + ".html";
                    c.v.folder && (j = j + "?f=" + c.v.folder.folderId);
                    var m = "";
                    h.encodevid == c.v.data.video.encodeid && (m = " class=selected");
                    h = "<li" + m + "><a touchstart=\"this.parentNode.className='selected'\" href=" + j + ">" + h.title.substr(0, 20) + "</a></li>";
                    g.push(h)
                }
                e[1] = g.join("");
                this._slbd.innerHTML = e.join("");
                e = "<div class=x-showlist-pages>;<span class=x-showlist-pre></span>;<ul>;;</ul>;<span class=x-showlist-next></span>".split(";");
                g = [];
                m = b.data.videos.previous ? parseInt(b.data.videos.previous.seq / 60) : 0;
                for (f = 0; f < (d.length - 1) / 60 + 1; f++) b = "",
                f == m && (b = " class=current"),
                h = "<li" + b + "><em>" + (f + 1) + "</em></li>",
                g.push(h);
                e[3] = g.join("");
                this._slft.innerHTML = e.join("")
            }
        },
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        bindEvent: function() {
            this.bind_close = c.bindAsEventListener(this, this.hide);
            c.addEventHandler(this._closeHandle, "click", this.bind_close);
            this.bind_toggle = c.bindAsEventListener(this, this.toggle);
            c.addEventHandler(this._showbtn, "click", this.bind_toggle)
        },
        removeEvent: function() {
            c.removeEventHandler(this._closeHandle, "click", this.bind_close)
        },
        hide: function() {
            this._showbtn.className = this._showbtn.className.replace(/[\s]*pressed/g, "");
            c.hide(this._showlist)
        },
        show: function() {
            this._showbtn.className += " pressed";
            c.show(this._showlist)
        },
        showListBtn: function() {
            if (c.v.data.videos) {
                var b = c.v.data.videos.list;
                null == b || 1 >= b.length || c.show(this._showbtn)
            } else c.hide(this._showbtn)
        },
        hideListBtn: function() {
            if (c.v.data.videos) {
                var b = c.v.data.videos.list;
                null == b || 0 == b.length || (c.hide(this._showbtn), this.hide())
            }
        },
        toggle: function(b) {
            "block" != this._showlist.style.display ? (this.show(), this.player._reporter.sendUserActionReport("xshl", "c"), f.Log(f.uniplayerUrl + u({
                e: "xshl",
                adr: f.isAndroid,
                ios: f.isIPAD
            }))) : this.hide();
            this.dispatch(b)
        },
        touchStart: function(b) {
            this._sx = b.targetTouches[0].clientX;
            this._sy = b.targetTouches[0].clientY;
            this._ex = this._sx;
            this._ey = this._ey
        },
        touchEnd: function() {},
        touchMove: function(b) {
            this._ex = b.targetTouches[0].clientX;
            this._ey = b.targetTouches[0].clientY;
            this._dx = this._ex - this._sx;
            this._dy = this._ey - this._sy;
            Math.abs(this._dx) > Math.abs(this._dy) || b.preventDefault()
        }
    };
    var wa = function(b) {
        this.player = b;
        this._handle = {};
        this._tips = c.get(".x-tips");
        c.hide(this._tips);
        this._tips.innerHTML = "<div class=x-tips-txt></div><div class=x-tips-close><a href=#><em>\u5173\u95ed</em></a></div><div class=x-tips-mask></div>";
        this._ptip = this._tips.getElementsByClassName("x-tips-txt")[0];
        this._ctip = this._tips.getElementsByClassName("x-tips-close")[0];
        null == n.getItem("youku_conf_skip") && n.setItem("youku_conf_skip", !0);
        this.bindEvent()
    };
    wa.prototype = {
        bindEvent: function() {
            c.addEventHandler(this._ctip, "click", c.bindAsEventListener(this, this.closeTip))
        },
        closeTip: function() {
            c.hide(this._tips);
            this.keepLastTime()
        },
        autoHide: function(b) {
            var c = this;
            setTimeout(function() {
                c.closeTip()
            },
            b)
        },
        keepLastTime: function() {},
        ignoreLastTime: function() {},
        isShowTimeTip: function() {
            var b = n.getItem("youku_keep_lasttime"),
            b = parseInt(b),
            c = n.getItem("youku_ignore_lasttime"),
            c = parseInt(c);
            return 3 <= b || 3 <= c ? !1 : !0
        },
        showLastTimeTip: function(b) {
            b = c.getTime(b);
            debug.log("last = " + b); ! 1 != this.isShowTimeTip() && (this._ptip.innerHTML = "\u4f18\u9177\u8bb0\u5fc6\u60a8\u4e0a\u6b21\u64ad\u653e\u5230<span class=x-tips-time>" + b + "</span>, <a class=x-tip-timebegin href=#>\u4ece\u5934\u89c2\u770b</a>", this._playBegin = this._ptip.getElementsByClassName("x-tip-timebegin")[0], c.addEventHandler(this._playBegin, "click", c.bindAsEventListener(this, this.seekBegin)), c.show(this._tips), this.autoHide(5E3))
        },
        onSkipTail: function() {
            "true" == n.getItem("youku_conf_skip") ? (this._ptip.innerHTML = "\u5373\u5c06\u4e3a\u60a8\u8df3\u8fc7\u7247\u5c3e, <a class=x-tip-skipnoway href=#>\u4e0d\u518d\u8df3\u8fc7</a>", this._skipnowtail = this._ptip.getElementsByClassName("x-tip-skipnoway")[0], c.addEventHandler(this._skipnowtail, "click", c.bindAsEventListener(this, this.skipNoway))) : (this._ptip.innerHTML = "\u662f\u5426\u8df3\u8fc7\u7247\u5934\u7247\u5c3e? <a class=x-tip-skipalways href=#>\u59cb\u7ec8\u8df3\u8fc7</a>", this._skipalwtail = this._ptip.getElementsByClassName("x-tip-skipalways")[0], c.addEventHandler(this._skipalwtail, "click", c.bindAsEventListener(this, this.skipAlways)));
            c.show(this._tips);
            this.autoHide(1E4)
        },
        onSkipHead: function() {
            "true" == n.getItem("youku_conf_skip") ? (this._ptip.innerHTML = "\u5df2\u7ecf\u4e3a\u60a8\u8df3\u8fc7\u7247\u5934, <a class=x-tip-skipnoway href=#>\u4e0d\u518d\u8df3\u8fc7</a>", this._skipnow = this._ptip.getElementsByClassName("x-tip-skipnoway")[0], c.addEventHandler(this._skipnow, "click", c.bindAsEventListener(this, this.skipNoway))) : (this._ptip.innerHTML = "\u662f\u5426\u8df3\u8fc7\u7247\u5934\u7247\u5c3e? <a class=x-tip-skipalways href=#>\u59cb\u7ec8\u8df3\u8fc7</a>", this._skipalw = this._ptip.getElementsByClassName("x-tip-skipalways")[0], c.addEventHandler(this._skipalw, "click", c.bindAsEventListener(this, this.skipImediately)));
            c.show(this._tips);
            this.autoHide(5E3)
        },
        onUglyAdPlay: function() {
            this._ptip.innerHTML = "\u5c0a\u656c\u7684\u4f1a\u5458\uff0c\u56e0\u7248\u6743\u539f\u56e0\uff0c\u8bf7\u70b9\u51fb\u53f3\u4e0a\u89d2 \u5173\u95ed\u5e7f\u544a ";
            c.show(this._tips);
            var b = this;
            setTimeout(function() {
                c.hide(b._tips)
            },
            15E3)
        },
        closeUglyHint: function() {
            c.hide(this._tips)
        },
        skipImediately: function() {
            debug.log("skip imediately");
            this.player._reporter.sendUserActionReport("xskh", "c");
            n.setItem("youku_conf_skip", !0);
            var b = parseInt((c.v.data.dvd || "").head) / 1E3;
            this.onSkipHead();
            this.player.seek(b);
            return ! 1
        },
        skipNoway: function() {
            this.player._reporter.sendUserActionReport("xnsk", "c");
            n.setItem("youku_conf_skip", !1);
            this._ptip.innerHTML = "\u8bbe\u7f6e\u6210\u529f";
            return ! 1
        },
        skipAlways: function() {
            this.player._reporter.sendUserActionReport("xask", "c");
            n.setItem("youku_conf_skip", !0);
            this._ptip.innerHTML = "\u8bbe\u7f6e\u6210\u529f";
            return ! 1
        },
        seekBegin: function() {
            this.player._reporter.sendUserActionReport("xseb", "c");
            c.hide(this._tips);
            this.ignoreLastTime();
            this.player.seek(0);
            return ! 1
        }
    };
    var V = function(b, c, e) {
        this.player = b;
        this.v = c;
        this.sid = e;
        this.isSendedConsumeReport = !1;
        f.hd = this.getHDFlag();
        if (0 < I.length) for (b = 0; b < I.length; b++) this.sendUepReport(I[b].type, I[b].time);
        this.dimension = {
            w: document.getElementById("x-player").offsetWidth,
            h: document.getElementById("x-player").offsetHeight
        };
        this.screenDim = {
            w: screen.availWidth,
            h: screen.availHeight
        }
    };
    V.prototype = {
        sendRecommendLog: function(b) {
            f.Log("http://r.l.youku.com/recclick?" + q(b))
        },
        tsInit: function() {
            this.tsSn = null
        },
        sendTSLog: function(b) {
            null == this.tsSn && (this.tsSn = 0);
            var d = 5,
            d = 24 < this.tsSn ? 20 : 12 < this.tsSn ? 10 : 5,
            e = this;
            this.tstimer = setTimeout(function() {
                e.sendTSLog(60)
            },
            1E3 * d);
            if (61 == b) clearTimeout(this.tstimer),
            this.tstimer = null;
            else if (e.player.video.paused) return;
            if (0 == this.tsSn) this.tsSn++;
            else {
                var g = c.v.data;
                g.sid = c.videoInfo._sid;
                c.initConfig.tslogconfig = c.initConfig.tslogconfig || {};
                var i = {};
                i.vvid = g.sid;
                i.vid = g.id;
                i.cf = this.getHDFlag();
                i.cpt = this.player.currentTime ? Math.floor(this.player.currentTime) : 0;
                i.full = this.player.controls.fullscreenPanel.fullFlag() ? 1 : 0;
                i.lang = this.getLanguage();
                i.pc = 60 == b ? 0 : 1;
                i.clb = 0;
                i.iku = "m";
                i.pt = this.getPlayTime();
                i.sn = this.tsSn++;
                i.hi = d;
                i.uid = c.v.data.user.uid;
                i.r = this.signTS(i.vvid + i.vid + i.cpt + i.pt + i.sn);
                f.Log("http://p-log.ykimg.com/tslog?" + q(i))
            }
        },
        signTS: function(b) {
            if (null == b) return 0;
            for (var c = 0,
            e = b.length,
            g = 0; g < e; g++) c = 43 * c + b.charCodeAt(g),
            c %= 1E10;
            return c
        },
        getPlayTime: function() {
            var b = 0;
            return b = 24 < this.tsSn ? 180 + 20 * (this.tsSn - 24) : 12 < this.tsSn ? 60 + 10 * (this.tsSn - 12) : 5 * this.tsSn
        },
        tslogparse: function() {},
        sendTSErrorLog: function() {},
        sendVVLog: function(b) {
            var d = c.v.data;
            d.sid = c.videoInfo._sid;
            c.initConfig.vvlogconfig = c.initConfig.vvlogconfig || {};
            var e = {
                pvid: ""
            };
            e.chid = d.video.category_id;
            e.url = encodeURI(this.getParentUrl() ? this.getParentUrl() : window.location.href);
            e.rurl = "";
            e.vvid = d.sid;
            e.vid = d.id;
            e.schid = d.video.category_id;
            e.plid = "";
            e.plchid = "";
            e.shid = null != d.show && d.show.id ? d.show.id: "";
            e.shchid = this.getSubCategories(d.video.subcategories);
            e.ptype = c.WIN_TYPE;
            e.cp = null != d.show && d.show.copyright ? d.show.copyright: "";
            e.vl = parseInt(d.video.seconds);
            e.cf = this.getHDFlag();
            e.hf = this.getMaxFileType();
            e.spt = 0;
            e.pb = 62 == b ? 2 : 0;
            e.vdoid = d.user.uid;
            e.out = "interior" == c.initConfig.wintype ? 0 : 1;
            e.r = this.signTS(e.vvid + e.vid);
            e.ext = this.getExtString(b);
            for (var g in c.initConfig.vvlogconfig) e[g] = c.initConfig.vvlogconfig[g];
            f.Log("http://v.l.youku.com/ykvvlog?" + q(e))
        },
        getSubCategories: function(b) {
            for (var c = "",
            e = 0; e < b.length; e++) c += b[e].id + "|";
            return c.substring(0, c.length - 1)
        },
        getLanguage: function() {
            null == this.langMap && (this.langMap = {
                "default": 1,
                guoyu: 1,
                yue: 2,
                chuan: 3,
                tai: 4,
                min: 5,
                en: 6,
                ja: 7,
                kr: 8,
                "in": 9,
                ru: 10,
                fr: 11,
                de: 12,
                it: 13,
                es: 14,
                th: 15,
                po: 16,
                man: 17,
                baby: 18
            });
            return this.langMap[c.defaultLanguage || "default"]
        },
        getExtString: function(b) {
            var d = {
                iku: "m"
            };
            d.full = this.player.controls.fullscreenPanel.fullFlag();
            d.lang = this.getLanguage();
            d.num = b;
            d.ctp = 0;
            d.pc = 60 == b ? 0 : 1;
            d.clb = 0;
            d. = "12";
            d.ev = "1";
            d.tk = f.userCache.token;
            d.oip = c.v.data.security.ip;
            d.isvip = c.v.data.user.vip ? "1": "0";
            d.paystate = this.getPayState();
            d.playstate = null == c.v.data.trial ? "1": "2";
            return encodeURI(q(d))
        },
        getPlayByType_: function(b) {
            var d = 0;
            62 == b && (d = 2);
            c.initConfig.vvlogconfig.pb && (d = c.initConfig.vvlogconfig.pb);
            return d
        },
        getMaxFileType: function() {
            var b = l._videoInfo._videoSegsDic;
            return b.hd2 ? 2 : b.mp4 ? 1 : 0
        },
        getHDFlag: function() {
            if (null == this.player) return 0;
            var b = null,
            d = this.player.video.src; - 1 != d.indexOf("m3u8") ? (b = {
                flv: 0,
                flvhd: 0,
                mp4: 1,
                hd2: 2,
                hd3: 3
            },
            d = c.defaultVideoType) : b = {
                "030020": 4,
                "030004": 0,
                "030008": 1,
                "030080": 3
            };
            for (var e in b) if ( - 1 !== d.indexOf(e)) return b[e];
            return 0
        },
        getParentUrl: function() {
            var b = null;
            if (parent !== window) try {
                b = parent.location.href
            } catch(c) {
                b = document.referrer
            }
            return b
        },
        addPlayerDurationReport: function(b) {
            var d = c.videoInfo;
            if (! (null == d || null == d._playListData)) {
                if (null == this.drtimer) {
                    var e = this;
                    this.drtimer = setInterval(function() {
                        e.player.video.paused || e.addPlayerDurationReport(60)
                    },
                    6E4)
                }
                61 == b && (clearInterval(this.drtimer), this.drtimer = null);
                var g = {
                    viewUserId: 0
                };
                g.sid = d._sid;
                g.videoOwnerId = c.v.data.video.userid;
                c.v.data.user.uid && (g.viewUserId = c.v.data.user.uid);
                g.videoid = c.v.data.id;
                g.ct = c.v.data.video.category_letter_id;
                g.cs = this.getSubCategories(c.v.data.video.subcategories);
                g.number = b;
                g.rnd = ((new Date).getTime() - d.abstarttime) / 1E3;
                null != d._playListData.show ? (g.showid_v2 = null == d._playListData.show ? "": d._playListData.show.id, g.showid_v3 = null == d._playListData.show ? "": d._playListData.show.encodeid, g.show_videotype = d._playListData.show.video_type, g.stg = d._playListData.show.stage, g.Copyright = d._playListData.show.copyright) : (g.showid_v2 = "", g.Copyright = "");
                g.Tid = "";
                g.hd = 0;
                g.ikuflag = "m";
                g.hd = {
                    flv: 0,
                    flvhd: 0,
                    mp4: 1,
                    hd2: 2,
                    hd3: 3
                } [c.defaultVideoType];
                g.winType = c.WIN_TYPE;
                g.mtype = $();
                g.totalsec = d.totalTime;
                g.fullflag = this.player.controls.fullscreenPanel.fullFlag();
                g.playComplete = 0;
                61 == b && (g.playComplete = 1);
                59 == b && (g.referUrl = (c.initConfig.vvlogconfig || "").rurl, g.url = encodeURIComponent(window.location.href), g.starttime = 0);
                g.currentPlayTime = parseInt(this.player.currentTime || 0);
                g.continuationPlay = 0;
                g.pid = c.initConfig.client_id;
                g.timestamp = (new Date).getTime();
                g.ctype = "12";
                g.ev = "1";
                g.tk = f.userCache.token;
                g.oip = c.v.data.security.ip;
                g.isvip = c.v.data.user.vip ? "1": "0";
                g.paystate = this.getPayState();
                g.playstate = null == c.v.data.trial ? "1": "2";
                f.Log("http://stat.youku.com/player/addPlayerDurationReport?" + q(g))
            }
        },
        addPlayerStaticReport: function() {
            var b = {};
            b.videoid = this.v.data.id;
            this.v.data.token && (b.t = this.v.data.token.vv);
            b.totalsec = parseInt(this.v.data.video.seconds);
            b.ikuflag = "m_" + this.getShowFlag();
            b.url = encodeURIComponent(this.getParentUrl() ? this.getParentUrl() : window.location.href);
            b.fullflag = this.player.controls.fullscreenPanel.fullFlag();
            b.source = "video";
            b.referer = (c.initConfig.vvlogconfig || "").rurl;
            b.sid = this.sid;
            b.uid = this.v.data.user.uid;
            for (var d = b.t,
            e = !1,
            g = ""; ! e;) {
                for (var g = "",
                i = 0; 20 > i; i++) var h = Math.floor(61 * Math.random()),
                g = g + "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz".substring(h, h + 1);
                "00" == Ca(d + g).substring(0, 2) && (e = !0)
            }
            b.h = g;
            b.totalseg = c.pieceLength();
            b = q(b);
            f.Log("http://stat.youku.com/player/addPlayerStaticReport?" + b)
        },
        sendUserActionReport: function(b, d, e) {
            d = {
                t: 1002,
                e: b,
                v: d
            };
            d.d = J($());
            var g = {
                v: "h5player",
                vid: c.v.data.id,
                ssid: c.videoInfo._sid,
                ct: c.v.data.video.category_letter_id,
                cs: c.v.data.video.subcategories,
                uid: 0
            };
            c.v.data.user && (g.uid = c.v.data.user.uid);
            g.sid = "";
            c.v.data.show && (g.sid = c.v.data.show.id);
            g.tc = this.player.currentTime || 0;
            g.w = c.get("#x-player").offsetWidth;
            g.h = c.get("#x-player").offsetHeight;
            g.f = this.player.video.fullscreenchange ? "on": "off";
            g.q = this.player.getQuality();
            g.ver = "1.0.0";
            for (var i in e) g[i] = e[i];
            d.x = J(q(g));
            i = q(d);
            if ("xre" == b) this.checkPlayerResize("http://e.stat.ykimg.com/red/ytes.php?", i);
            else {
                if ("xenfs" == b || "xexfs" == b) {
                    this._giveupReTag = !0;
                    var h = this;
                    setTimeout(function() {
                        h._giveupReTag = false
                    },
                    800)
                }
                f.Log("http://p-log.ykimg.com/event?" + i)
            }
            this.sendCustomUserAction(b, e)
        },
        checkScreenRotate: function(b, c) {
            var e = screen.availWidth,
            g = screen.availHeight;
            debug.log("<hr/>rota w,h = " + e + "," + g);
            if (this.screenDim.w != e || this.screenDim.h != g) this.screenDim.w = e,
            this.screenDim.h = g,
            debug.log("<b><font color=red>rotate</font></b>"),
            f.Log(b + c)
        },
        checkPlayerResize: function(b, c) {
            if (!0 === this._giveupReTag) debug.log("give up xre after enfs or exfs");
            else {
                var e = document.getElementById("x-player");
                this._resizeList = this._resizeList || [];
                this._resizeList.push({
                    str: c,
                    time: (new Date).getTime(),
                    w: e.offsetWidth,
                    h: e.offsetHeight
                });
                var g = this;
                setTimeout(function() {
                    if (0 != g._resizeList.length) {
                        for (var c = g._resizeList[0].time, d = 0; d < g._resizeList.length; d++) {
                            var e = g._resizeList[d].w,
                            m = g._resizeList[d].h,
                            l = g._resizeList[d].time;
                            if (e != g.dimension.w || m != g.dimension.h) g.dimension.w = e,
                            g.dimension.h = m,
                            (800 < l - c || d == g._resizeList.length - 1) && f.Log(b + g._resizeList[d].str)
                        }
                        g._resizeList = []
                    }
                },
                1E3)
            }
        },
        sendCustomUserAction: function(b, c) {
            var e = {
                e: b
            },
            g;
            for (g in c) e[g] = c[g];
            e.device = f.isAndroid ? "adr": f.isIPAD ? "ipad": "oth";
            switch (b) {
            case "xenfs":
                f.Log(f.uniplayerUrl + u(e));
                break;
            case "xexfs":
                f.Log(f.uniplayerUrl + u(e));
                break;
            case "xsra":
                f.Log(f.uniplayerUrl + u(e))
            }
        },
        sendCustomLoadedTime: function(b) {
            b = {
                vid: c.v.data.id,
                os: encodeURI(f.os),
                adrd4: f.isAndroid4,
                mobile: f.isMobile,
                type: "mp4" == c.config.content ? c.defaultVideoType: c.config.content,
                cost: b,
                ver: "2015/11/2510:21:25".replace(/[-:]/g, "")
            }; ! 1 == b.mobile && (b.ua = encodeURI(navigator.userAgent.replace(/[\/\+\*@\(\)\,]/g, "")));
            f.Log("http://passport-log.youku.com/logsys/logstorage/append?project=xplayerloadtime&log=" + u(b))
        },
        sendUepReport: function(b, d, e) { ! 1 !== e && 10 < 100 * Math.random() || (e = "", e = f.isIPAD ? "xplayer_ipad": f.isIPHONE ? "xplayer_iphone": "xplayer_android", b = {
                m: e,
                hd: this.getHDFlag(),
                t: b,
                s: d,
                u: encodeURIComponent(this.getParentUrl() ? this.getParentUrl() : window.location.href),
                p: 2,
                v: c.videoInfo._sid,
                ct: c.v.data.video.category_letter_id,
                cs: c.v.data.video.subcategories
            },
            f.Log("http://v.l.youku.com/uep?" + q(b)))
        },
        sendLoadedTime: function(b) {
            debug.log("loaded cost = " + b);
            this.sendCustomLoadedTime(b);
            this.sendUepReport("videoload", b)
        },
        sendComScoreReport: function(b) {
            if (!this._hasComScore) {
                for (var d = document.getElementsByTagName("script"), e = 0; e < d.length; e++) if ( - 1 !== d[e].src.indexOf("scorecardresearch.com/beacon.js")) {
                    this._hasComScore = !0;
                    break
                } ! 0 !== this._hasComScore && (d = document.createElement("script"), e = document.getElementsByTagName("script")[0], d.async = !0, d.src = ("https:" == document.location.protocol ? "https://sb": "http://b") + ".scorecardresearch.com/beacon.js", e.parentNode.insertBefore(d, e));
                this._hasComScore = !0
            }
            var g = setInterval(function() {
                if ("undefined" != typeof COMSCORE) {
                    clearInterval(g);
                    try {
                        COMSCORE.beacon({
                            c1: 1,
                            c2: 7293931,
                            c3: b,
                            c6: c.v.data.video.category_id
                        })
                    } catch(d) {
                        debug.log("beacon exception")
                    }
                }
            },
            500)
        },
        sendIResearchReport: function() {},
        sendThirdPartyReport: function(b) {
            "xplayer_h5" == b && (b = f.isAndroid ? "xplayer_h5_android": f.isIPAD ? "xplayer_h5_ipad": "xplayer_h5_other");
            this.sendComScoreReport(b);
            this.sendIResearchReport(b)
        },
        sendPayReport: function() {
            var b = {
                vid: c.v.data.id,
                os: encodeURI(f.os)
            };
            f.Log("http://passport-log.youku.com/logsys/logstorage/append?project=unipay&log=" + u(b))
        },
        sendClientConsumeReport: function() { ! 0 != this.isSendedConsumeReport && (null != c.config.partner_config && 1 == c.config.partner_config.status && null != c.config.partner_config.token && "" != c.config.partner_config.token) && (this.isSendedConsumeReport = !0, f.Log("https://api.youku.com/players/consume.json?token=" + c.config.partner_config.token))
        },
        getPayState: function() {
            var b = 0;
            c.v.data.show && "vod" == c.v.data.show.pay_type && (b = 1);
            c.v.data.show && "mon" == c.v.data.show.pay_type && (b = 2);
            return b
        },
        getShowFlag: function() {
            var b = "m";
            return b = c.v.data.show ? b + "1": b + "0"
        }
    };
    var xa = function(b, c) {
        this._handler = {};
        this._adinfo = b;
        this._info = {
            VAL: []
        };
        for (var e in b)"VAL" != e && (this._info[e] = b[e]);
        this._vt2nodes = c || []
    };
    xa.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        buildAdRS: function() {
            for (var b = "http://pl.youku.com/playlist/m3u8?",
            d = {},
            e = {},
            g = this._adinfo.VAL,
            i = 0; i < g.length; i++) {
                var h = g[i];
                e["a" + (i + 1)] = h.VID + "_" + h.VQT
            }
            e.v = c.v.data.id + "_" + c.defaultVideoType;
            var i = encodeURI,
            h = [],
            j;
            for (j in e) h.push('"' + j + '":"' + e[j] + '"');
            e = "{" + h.join(",") + "}";
            d.ids = i(e);
            d.ts = parseInt((new Date).getTime() / 1E3);
            c.password && (d.password = c.password);
            c.password && (c.initConfig.client_id && c.config.partner_config && 1 == c.config.partner_config.status && 1 == c.config.partner_config.passless) && (d.client_id = c.initConfig.client_id);
            e = [];
            for (j = 0; j < g.length; j++) e.push(g[j].VID);
            e.push(c.v.data.id);
            g = encodeURIComponent(J(L(M(c.mk.a4 + "poz" + f.userCache.a2, [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), f.userCache.sid + "_" + e.join("") + "_" + f.userCache.token)));
            d.ep = g;
            d.sid = f.userCache.sid;
            d.token = f.userCache.token;
            d.ctype = "12";
            d.ev = "1";
            d.oip = c.v.data.security.ip;
            b += q(d);
            "" != c.getUCStr(c.v.data.id) && (b += c.getUCStr(c.v.data.id));
            return b
        },
        run: function() {
            if (! (null == this._adinfo || null == this._adinfo.VAL || 0 == this._adinfo.VAL.length)) {
                for (var b = {
                    SUS: [],
                    SU: [],
                    SUE: [],
                    CU: [],
                    CUM: [],
                    VTVC: []
                },
                c = 0, e = 0; e < this._adinfo.VAL.length; e++) {
                    var g = this._adinfo.VAL[e];
                    if (! (null == g.VID || null == g.VQT)) {
                        null == g.SU && (g.SU = []);
                        null == g.SUE && (g.SUE = []);
                        if (0 == e) b.SUS = g.SUS || [];
                        else for (var f = 0; f < g.SUS.length; f++) b.SU.push({
                            T: c,
                            U: g.SUS[f].U
                        });
                        for (f = 0; f < g.SU.length; f++) {
                            var h = g.SU[f].T + c;
                            b.SU.push({
                                T: h,
                                U: g.SU[f].U
                            })
                        }
                        if (e == this._adinfo.VAL.length - 1) b.SUE = g.SUE;
                        else for (f = 0; f < g.SUE.length; f++) h = c + g.AL,
                        b.SU.push({
                            T: h,
                            U: g.SUE[f].U
                        });
                        c += g.AL;
                        b.CU.push({
                            T: c,
                            U: g.CU
                        });
                        b.CUM.push({
                            T: c,
                            CUM: g.CUM
                        });
                        1 == parseInt(g.VT) && b.VTVC.push({
                            U: g.VC,
                            T: c
                        });
                        if (0 != this._vt2nodes.length) for (f = 0; f < this._vt2nodes.length; f++) g = this._vt2nodes[f].VC,
                        h = this._vt2nodes[f].pos_,
                        -1 == h && b.VTVC.push({
                            U: g,
                            T: 0
                        }),
                        h == e && b.VTVC.push({
                            U: g,
                            T: c
                        })
                    }
                }
                b.AL = c;
                b.RS = this.buildAdRS();
                this._info.VAL.push(b);
                this._info.src = b.RS
            }
            this.dispatch({
                type: P,
                data: this._info
            })
        }
    };
    var W = function(b, c) {
        this._handler = {};
        this.player = b;
        this.video = this.player.video;
        this.controls = this.player.controls;
        this._adplugin = this.player._adplugin;
        this._adplugin.adplayer = this;
        this.video.preload = "none";
        this.video.src = c.data.urls[0];
        debug.log("ad src=" + this.video.src);
        this.video.style.display = "block";
        this._addata = c.data;
        this._addata.curnum = 0;
        this._playTag = [];
        this.bindAdEvent();
        this._adreporter = new N(this, this._addata)
    };
    W.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        bindAdEvent: function() {
            this.bind_fadtoplay = c.bindAsEventListener(this, this.onPlayClick);
            this.bind_fadplay = c.bindAsEventListener(this, this.onAdPlay);
            this.bind_fadended = c.bindAsEventListener(this, this.onAdEnded);
            this.bind_faderror = c.bindAsEventListener(this, this.onAdError);
            this.bind_fadpause = c.bindAsEventListener(this, this.onAdPause);
            this.bind_fadsuspend = c.bindAsEventListener(this, this.onAdSuspend);
            this.bind_fadstalled = c.bindAsEventListener(this, this.onAdStalled);
            this.bind_fadwaiting = c.bindAsEventListener(this, this.onAdWaiting);
            this.bind_fadloadedmetadata = c.bindAsEventListener(this, this.onAdLoadedMetaData);
            this.bind_fadtimeupdate = c.bindAsEventListener(this, this.onAdTimeUpdate);
            c.addEventHandler(this.video, "play", this.bind_fadplay);
            c.addEventHandler(this.video, "ended", this.bind_fadended);
            c.addEventHandler(this.video, "error", this.bind_faderror);
            c.addEventHandler(this.video, "pause", this.bind_fadpause);
            c.addEventHandler(this.video, "suspend", this.bind_fadsuspend);
            c.addEventHandler(this.video, "stalled", this.bind_fadstalled);
            c.addEventHandler(this.video, "waiting", this.bind_fadwaiting);
            c.addEventHandler(this.video, "loadedmetadata", this.bind_fadloadedmetadata);
            c.addEventHandler(this.video, "timeupdate", this.bind_fadtimeupdate);
            this.shadow = this.controls.buttons.shadow;
            this.videobtn = this.controls.buttons.videobtn;
            c.addEventHandler(this.videobtn, "click", this.bind_fadtoplay, !0)
        },
        removeAdEvent: function() {
            c.removeEventHandler(this.video, "play", this.bind_fadplay);
            c.removeEventHandler(this.video, "ended", this.bind_fadended);
            c.removeEventHandler(this.video, "error", this.bind_faderror);
            c.removeEventHandler(this.video, "pause", this.bind_fadpause);
            c.removeEventHandler(this.video, "suspend", this.bind_fadsuspend);
            c.removeEventHandler(this.video, "stalled", this.bind_fadstalled);
            c.removeEventHandler(this.video, "waiting", this.bind_fadwaiting);
            c.removeEventHandler(this.video, "timeupdate", this.bind_fadtimeupdate);
            c.removeEventHandler(this.video, "loadedmetadata", this.bind_fadloadedmetadata);
            c.removeEventHandler(this.videobtn, "click", this.bind_fadtoplay, !0)
        },
        onPlayClick: function() {
            this.video.play()
        },
        checkVTVC: function(b) {
            var c = this._addata.vtvc;
            if (! (null == c || 0 === c.length)) for (var e = 0; e < c.length; e++) {
                var g = c[e];
                g.pos_ == b - 1 && C(g.VC, "js")
            }
        },
        play: function() {
            this.checkVTVC(0);
            this.video.load();
            this.video.play()
        },
        leftSecond: function() {
            for (var b = this._addata.curnum,
            c = this._addata.seconds.length,
            e = this._addata.seconds[b] - this.video.currentTime, b = b + 1; b < c; b++) e += this._addata.seconds[b];
            return parseInt(e)
        },
        clearTimer: function() {
            clearInterval(this._checkTimer);
            this._checkTimer = null
        },
        checkPause: function() {
            if (!this._checkTimer) {
                var b = this;
                this._timelist = [];
                this._checkTimer = setInterval(function() {
                    if (b.video.paused) b.onAdPause();
                    else b._timelist.push(b.video.currentTime),
                    3 <= b._timelist.length && (1 > Math.abs(b._timelist[0] - b._timelist[2]) && (debug.log("<b>ad unexpected pause</b>"), b.video.play(), 0 == b.leftSecond() && (debug.log("<b>exception left = 0 </b>"), b.onAdEnded())), b._timelist = [])
                },
                1E3)
            }
        },
        onAdPlay: function() {
            this.checkPause();
            var b = this.controls.container.poster;
            c.hide(this.controls.buttons.videobtn);
            c.hide(b);
            c.hide(c.get(".x-video-info"));
            this.video.style.display = "block";
            b = this._addata.curnum;
            debug.log("left=" + this.leftSecond() + " curtotal=" + this._addata.seconds[b] + " curtime=" + this.video.currentTime);
            this._adplugin.setLeftSecond(this.leftSecond());
            var d = this;
            setTimeout(function() {
                debug.log("ad media timeout check begin = " + d._adBegin);
                d._adBegin || (d.removeAdEvent(), d._adplugin.hide(), d._adplugin.reportTime("advideo", -1, !1), d.dispatch({
                    type: z,
                    data: !0
                }))
            },
            1E4);
            this._playTag[b] || (this._playTag[b] = !0, this._adfirsttu = !1, this._adplugin.recordTime("advideo"), n.appendItem("phase", "adplay"))
        },
        uglyClose: function() {
            this.video.src = "";
            this.video.load();
            this.video.play()
        },
        onAdError: function() {
            this.checkVTVC(this._addata.curnum + 1);
            this.removeAdEvent();
            this._adplugin.hide();
            this._adplugin.reportTime("advideo", -1, !1);
            this.dispatch({
                type: z,
                data: !0
            })
        },
        onAdEnded: function(b) {
            debug.log("ad ended");
            this._adreporter.sendSUE();
            this.checkVTVC(this._addata.curnum + 1);
            if (this._addata.curnum < this._addata.urls.length - 1) this.onMiddleAdEnded(b);
            else this.removeAdEvent(),
            this._adplugin.hide(),
            this.clearTimer(),
            this.dispatch({
                type: B,
                data: !0
            }),
            n.appendItem("phase", "adend")
        },
        onMiddleAdEnded: function() {
            debug.log("onMiddleAdEnded");
            this._pauseLeftSec = !0;
            var b = this;
            setTimeout(function() {
                b._pauseLeftSec = !1
            },
            1E3);
            this._addata.curnum++;
            this.video.src = this._addata.urls[this._addata.curnum];
            this.video.load();
            this.video.play();
            this._adBegin = !1
        },
        onAdPause: function() {
            this.player.video.ended || (c.show(this.controls.buttons.videobtn), c.hide(this.controls.buttons.shadow))
        },
        onAdSuspend: function() {
            debug.log("<font color=red>ad suspend</font>")
        },
        onAdStalled: function() {
            debug.log("<font color=red>ad stalled</font>")
        },
        onAdWaiting: function(b) {
            this.controls.onWaiting(b)
        },
        onAdTimeUpdate: function() {
            c.hide(this.controls.buttons.loading);
            this._adBegin = !0;
            c.hide(this.controls.buttons.loading);
            this._pauseLeftSec || this._adplugin.setLeftSecond(this.leftSecond());
            this._adreporter.sendSU(this.video.currentTime);
            0.5 <= this.video.currentTime && this._adplugin.show();
            this._adfirsttu || (this._adfirsttu = !0, this._adreporter.sendSUS(), this._adreporter.sendVC(), this._adplugin.reportTime("advideo"), f.isNeedAdrTrick() && f.adrInvalidPauseCheck(this.video), 0 === this._adplugin.SKIP && this.dispatch({
                type: G
            }))
        },
        onAdLoadedMetaData: function() {
            this._adBegin = !0
        },
        onAdClick: function() {
            this.video.pause();
            this._adreporter.sendCUM();
            var b = this._addata,
            b = b.info.VAL[b.curnum].CU;
            debug.log("click cu=" + b);
            window.open(b, "", "", !1)
        }
    };
    B = "adend";
    z = "aderror";
    P = "frontAdinfoadapterok";
    G = void 0;
    var X = function(b, d, e) {
        this._handler = {};
        this.player = b;
        this.sid = e;
        this._advids = [];
        this._adsecs = [];
        this._adsrcs = [];
        this._vid = d.data.video.encodeid;
        this._advert = c.get(".x-advert");
        this._adskip = this._advert.getElementsByClassName("x-advert-skip")[0];
        this._adcount = this._advert.getElementsByClassName("x-advert-countdown")[0];
        this._adknowdet = this._advert.getElementsByClassName("x-advert-detail")[0];
        this.init(d);
        this.bindEvent()
    };
    X.prototype = {
        init: function(b) {
            this.initRequestParam(b);
            this._adskipTxt = this._adskip.getElementsByClassName("x-advert-txt")[0];
            this._adskipTxt.innerHTML = "\u8df3\u8fc7\u5e7f\u544a";
            this._adcountTxt = this._adcount.getElementsByClassName("x-advert-txt")[0];
            this._adcountTxt.innerHTML = "\u5e7f\u544a <span class=x-advert-sec></span> \u79d2";
            this._adsec = this._adcountTxt.getElementsByClassName("x-advert-sec")[0]
        },
        getSubCategories: function(b) {
            for (var c = "",
            e = 0; e < b.length; e++) c += b[e].id + "|";
            return c.substring(0, c.length - 1)
        },
        initRequestParam: function(b) {
            var d = {
                site: 1,
                p: 0,
                vl: parseInt(b.data.video.seconds),
                fu: 0,
                ct: b.data.video.category_letter_id,
                cs: this.getSubCategories(b.data.video.subcategories),
                d: 0,
                paid: b.data.show ? b.data.show.pay: 0,
                s: b.data.show ? b.data.show.id: 0,
                sid: this.sid,
                td: b.data.video.source ? b.data.video.source: 0,
                v: b.data.id,
                vip: b.data.user.vip ? 1 : 0,
                wintype: "xplayer_m3u8",
                u: b.data.video.userid,
                bt: f.isPad ? "pad": "phone",
                os: f.isMobileIOS ? "ios": "Android",
                rst: f.isMobileIOS ? "m3u8": "3gphd",
                tict: 0,
                aw: "w",
                vs: "1.0"
            };
            null != c.config.partner_config && (d.partnerid = c.initConfig.client_id, d.atm = c.config.partner_config.atm);
            for (var e in c.initConfig.adconfig) d[e] = c.initConfig.adconfig[e];
            this._param = d;
            this._ti = encodeURIComponent(b.data.video.title);
            this._k = encodeURIComponent((b.data.video.tags || []).join("|"));
            this.loadPartnerParam()
        },
        loadPartnerParam: function() {},
        partnerParse: function() {},
        initRequestParam_: function(b) {
            var d = {
                ct: b.data.video.category_letter_id,
                cs: b.data.video.subcategories,
                v: b.data.id,
                t: parseInt(b.data.video.seconds),
                u: b.data.video.userid,
                fileid: "todo",
                winType: "xplayer_m3u8",
                partnerid: c.config.partnerId,
                sid: this.sid,
                k: "",
                td: "todo"
            };
            d.s = b.data.show ? b.data.show.id: "";
            b.user && (d.vip = b.data.user.vip ? 1 : 0);
            d.paid = b.data.show ? b.data.show.pay: 0;
            for (var e in c.initConfig.adconfig) d[e] = c.initConfig.adconfig[e];
            this._param = d
        },
        bindEvent: function() {
            var b = this;
            this.fSkipAd = function() {
                b.adplayer.video.pause();
                window.open("http://cps.youku.com/redirect.html?id=000002bf", "", "", !1)
            };
            this._adskip.addEventListener("click", this.fSkipAd, !1);
            this._adknowdet.addEventListener("click",
            function() {
                debug.log("detail clicked");
                b.adplayer.onAdClick("")
            },
            !1)
        },
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        show: function() {
            c.show(this._advert)
        },
        hide: function() {
            c.hide(this._advert)
        },
        setLeftSecond: function(b) {
            debug.log(b);
            this._adsec && (this._adsec.innerText = b)
        },
        splitVTVC: function(b) {
            debug.log("split adinfo vt vc");
            this._vtvc = [];
            var c = {},
            e;
            for (e in b)"VAL" != e && (c[e] = b[e]);
            c.VAL = [];
            b = b.VAL;
            for (e = 0; e < b.length; e++) 2 === parseInt(b[e].VT) ? (b[e].pos_ = e - 1 - this._vtvc.length, this._vtvc.push(b[e])) : null == b[e].RS || ("" == b[e].RS.trim() || null == b[e].VID || null == b[e].VQT) || c.VAL.push(b[e]);
            return c
        },
        buildTestData: function() {
            return {
                VAL: [{
                    AL: 15,
                    VID: 147660115,
                    VQT: "flv",
                    SUS: [{
                        U: "http://mytestdata.com1"
                    },
                    {
                        U: "http://mytestdata.com2"
                    }],
                    SU: [],
                    SUE: [],
                    CU: "http://www.baidu.com",
                    CUM: [{
                        U: "http://cum"
                    }],
                    RS: "http://fasdfa"
                },
                {
                    AL: 15,
                    VID: 15252,
                    VQT: "flv",
                    SUS: [{
                        U: "http://mytestdata.com1"
                    },
                    {
                        U: "http://mytestdata.com2"
                    }],
                    SU: [],
                    SUE: [],
                    CU: "http://www.bing.com",
                    CUM: [{
                        U: "http://cum"
                    }],
                    RS: "http://fasdfa",
                    VT: 2,
                    VC: "http://vc.com"
                }]
            }
        },
        checkSkip: function(b) {
            b && 0 === parseInt(b.SKIP) && (c.hide(this._adskip), this.SKIP = 0)
        },
        adParseUnited: function(b) {
            this.checkSkip(b);
            this._isAdInfoOk = !0;
            n.appendItem("phase", "adinfo");
            this.reportTime("adinfo");
            b && b.VAL && (debug.log("<b>before split val length =  " + b.VAL.length + "</b>"), b = this.splitVTVC(b), debug.log("<b>after : val length =  " + b.VAL.length + "</b>"));
            if (null == b || null == b.VAL || 0 == b.VAL.length) b = {
                VAL: []
            },
            this.dispatch({
                type: "unitedfrontadinfook",
                data: {
                    info: {
                        VAL: []
                    },
                    vtvc: this._vtvc || []
                }
            });
            else {
                var b = new xa(b, this._vtvc),
                c = this;
                b.addEventListener(P,
                function(b) {
                    debug.log("ad info adapter ok");
                    c.dispatch({
                        type: "unitedfrontadinfook",
                        data: {
                            info: b.data,
                            vtvc: c._vtvc || []
                        }
                    })
                });
                b.run()
            }
        },
        adParse: function(b) {
            this.checkSkip(b);
            n.appendItem("phase", "adinfo");
            this.reportTime("adinfo");
            this._isAdInfoOk = !0;
            if (b && b.VAL) for (var b = this.splitVTVC(b), c = b.VAL, e = 0; e < c.length; e++) this._adsrcs.push(c[e].RS),
            this._adsecs.push(parseInt(c[e].AL));
            debug.log("frontad len =" + this._adsrcs.length);
            this.dispatch({
                type: "frontAdinfook",
                data: {
                    ids: this._advids || [],
                    urls: this._adsrcs,
                    seconds: this._adsecs,
                    info: b,
                    vtvc: this._vtvc || []
                }
            })
        },
        buildPauseData: function() {
            return adinfo = {
                P: 10,
                VAL: [{
                    RS: "http://static.atm.youku.com/Youku2013/201307/0715/27896/600-430.jpg",
                    RST: "img",
                    AT: 73,
                    SU: [],
                    SUS: [{
                        U: "http://mf.atm.youku.com/mshow?v=137006183&at=73&ct=d&cs=1003&ca=135159&ie=150597&uid=1234567&ck=137689524489061H&al=0&bl=1&s=&td=&st=1&vl=1200.0&ap=4&sid=1&cr=0&tvb=0&pr=100&oidtype=27896%7C1&tpa=null&rid=&os=1&dt=1&aw=a&avs="
                    }],
                    SUE: [],
                    CU: "http://vid.atm.youku.com/mclick?v=137006183&at=73&ct=d&cs=1003&ca=135159&ie=150597&uid=1234567&ck=137689524489061H&al=0&bl=1&s=&td=&st=1&vl=1200.0&ap=4&sid=1&cr=0&tvb=0&pr=100&oidtype=27896%7C1&tpa=null&rid=&os=1&dt=1&aw=a&avs=&u=http://static.youku.com/pub/youku/fragment/panel_phone.html&md5=f2450cd80597324b57d986147dc1b3a9",
                    W: 400,
                    H: 300,
                    CF: "1"
                }]
            }
        },
        adParsePause: function(b) {
            debug.log("<b> ad parse pause </b>");
            n.appendItem("phase", "pauseadinfo");
            this.reportTime("adinfo");
            this._isPauseAdInfoOk = !0;
            null == b || null == b.VAL || 0 == b.VAL.length || 10 != b.P ? this.dispatch({
                type: "pauseAdinfoerror"
            }) : (debug.log("<b>pause ad len = " + b.VAL.length + "</b>"), this.dispatch({
                type: "pauseAdinfook",
                data: {
                    info: b
                }
            }))
        },
        frontAd: function() {
            this._param.fu = this.player.controls.fullscreenPanel.fullFlag() ? 1 : 0;
            this._param.p = 7;
            this._param.callback = "adpluginobject.adParse";
            c.OLD_M3U8 = !0;
            f.isIPAD && (debug.log("<font color=red> new m3u8 api</font>"), c.OLD_M3U8 = !1, this._param.callback = "adpluginobject.adParseUnited");
            var b = "http://mf.atm.youku.com/mf?" + q(this._param) + "&ti=" + this._ti + "&k=" + this._k;
            A(b);
            this.recordTime("adinfo");
            var d = this;
            setTimeout(function() {
                if (!d._isAdInfoOk) {
                    debug.log("adinfo timeout");
                    d.reportTime("adinfo", -1);
                    d.dispatch({
                        type: "frontAdinfotimeout",
                        data: {
                            timeout: 8E3
                        }
                    })
                }
            },
            8E3)
        },
        pauseAd: function() {
            this._param.r_ = parseInt(1E4 * Math.random());
            this._param.p = 10;
            this._param.fu = this.player.controls.fullscreenPanel.fullFlag() ? 1 : 0;
            this._param.callback = "adpluginobject.adParsePause";
            var b = "http://mp.atm.youku.com/mp?" + q(this._param) + "&ti=" + this._ti + "&k=" + this._k;
            A(b);
            this.recordTime("adinfo");
            var c = this;
            setTimeout(function() {
                c._isPauseAdInfoOk || (debug.log("pause ad info timeout"), c.reportTime("adinfo", -1), c.dispatch({
                    type: "pauseadinfotimeout",
                    data: {
                        timeout: 8E3
                    }
                }))
            },
            8E3)
        },
        recordTime: function(b) {
            null == this._timearr && (this._timearr = {});
            this._timearr[b] = (new Date).getTime()
        },
        reportTime: function(b, c, e) {
            null == this._timearr && (this._timearr = {});
            c = c || (new Date).getTime() - this._timearr[b];
            this.player._reporter.sendUepReport({
                adinfo: "valfload",
                advideo: "adload"
            } [b], c, e)
        },
        backAd: function() {
            this._param.fu = this.player.controls.fullscreenPanel.fullFlag();
            this._param.p = 9;
            this._param.callback = "adpluginobject.adParse";
            this._param.ctu = 0;
            var b = "http://mb.atm.youku.com/mb?" + q(this._param) + "&ti=" + this._ti + "&k=" + this._k;
            A(b);
            var c = this;
            setTimeout(function() {
                c._isAdInfoOk || (debug.log("adinfo timeout"), c.dispatch({
                    type: " backAdinfotimeout",
                    data: {
                        timeout: 5E3
                    }
                }))
            },
            5E3)
        },
        insertAd: function() {
            this._param.ps = 0;
            this._param.pt = 0
        }
    };
    var N = function(b, c) {
        this.adplayer = b;
        this.addata = c;
        "undefined" == typeof c.curnum && (this.addata.curnum = 0)
    };
    N.prototype = {
        sendSUS: function() {
            var b = this.addata.info.VAL[this.addata.curnum].SUS;
            if ("undefined" != typeof b) for (var c = 0; c < b.length; c++) f.Log(b[c].U)
        },
        sendUnitedVTVC: function(b) {
            var b = b + 2,
            c = this.addata.info.VAL[0].VTVC;
            this._vtccache || (this._vtccache = []);
            for (var e = null,
            g = 1E6,
            f = 1E5,
            h = 0; h < c.length; h++) {
                var j = c[h].U,
                m = parseInt(c[h].T),
                l = b - m;
                0 <= l && l < f && (f = l, e = j, g = m)
            }
            null != e && -1 == this._vtccache.indexOf(g) && (this._vtccache.push(g), debug.log("<b> vc = " + e + "</b>"), C(e, "js"))
        },
        sendVC: function() {
            var b = this.addata.info.VAL[this.addata.curnum];
            "undefined" != typeof b.VT && C(b.VC, "js")
        },
        sendSUS_: function() {
            var b = this.addata.info,
            c = this.addata.curnum + 2,
            e = b["A" + c].ATMSU,
            g = b["A" + c].ISOSU;
            f.Log(b["A" + c].SU);
            f.Log(e);
            f.Log(g)
        },
        sendSUE: function() {
            var b = this.addata.info.VAL[this.addata.curnum].SUE;
            if ("undefined" != typeof b) for (var c = 0; c < b.length; c++) f.Log(b[c].U)
        },
        sendSUE_: function() {
            var b = this.addata.info,
            c = this.addata.curnum + 2,
            e = b["A" + c].COU;
            f.Log(b["A" + c].OU);
            f.Log(e)
        },
        sendSU: function(b) {
            var c = this.addata.info.VAL[this.addata.curnum].SU;
            if ("undefined" != typeof c) {
                this._sucache || (this._sucache = []);
                for (var e = 1E4,
                g = 1E6,
                i = 0; i < c.length; i++) {
                    var h = parseInt(c[i].T),
                    j = b - h;
                    0 <= j && j < e && (e = j, g = h)
                }
                if (1E6 != g && -1 == this._sucache.indexOf(g)) {
                    this._sucache.push(g);
                    for (i = 0; i < c.length; i++) parseInt(c[i].T) == g && f.Log(c[i].U)
                }
            }
        },
        sendSU_: function(b) {
            var c = c + 2,
            e = this.addata.info["A" + c].MT;
            e && b >= parseInt(e) && (b = this.addata.info["A" + c].CMU, f.Log(this.addata.info["A" + c].MU), f.Log(b))
        },
        sendCUM: function() {
            var b = this.addata.info.VAL[this.addata.curnum].CUM;
            if ("undefined" != typeof b) for (var c = 0; c < b.length; c++) f.Log(b[c].U)
        },
        sendUnitedCUM: function(b) {
            var c = this.addata.info.VAL[0].CUM;
            if (! ("undefined" == typeof c || 0 === c.length)) for (var e = 0; e < c.length; e++) if (b < parseInt(c[e].T)) {
                for (b = 0; b < (c[e].CUM || []).length; b++) f.Log(c[e].CUM[b].U);
                break
            }
        },
        sendCUM_: function() {
            var b = this.addata;
            f.Log(b.info["A" + (b.curnum + 2)].VCU)
        }
    };
    var ya = function(b, d) {
        this._handler = {};
        this.player = b;
        this.controls = b.controls;
        this.adplugin = this.controls._pauseAdPlugin;
        this.info = d.data.info;
        this.adjustIMGWH();
        this.adpause = c.get(".x-ad-pause");
        this.info.VAL[0].VT = parseInt(this.info.VAL[0].VT);
        2 != this.info.VAL[0].VT && (this.init(), this.bindEvent(), this._adreporter = new N(this, d.data));
        this.loadVC()
    };
    ya.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        bindEvent: function() {
            c.addEventHandler(this.adcontent, "click", c.bindAsEventListener(this, this.adClick));
            c.addEventHandler(this.adclose, "click", c.bindAsEventListener(this, this.hide));
            var b = this;
            window.addEventListener("orientationchange",
            function() {
                setTimeout(function() {
                    c.isLandScape() || b.hide()
                },
                1E3)
            })
        },
        adjustIMGWH: function() {
            var b = this.info.VAL[0].W,
            d = this.info.VAL[0].H,
            e = (c.get("#x-player").offsetHeight - 110) / d;
            if (1 < e || 0 >= e) e = 1;
            this.info.VAL[0].W = b * e;
            this.info.VAL[0].H = d * e;
            debug.log("pause img adjusted w = " + this.info.VAL[0].W + " h = " + this.info.VAL[0].H)
        },
        init: function() {
            this.adpause.innerHTML = "<div class=x-pause-content></div><div class=x-pause-close></div><div class=x-pause-prompt></div>";
            this.adcontent = this.adpause.getElementsByClassName("x-pause-content")[0];
            this.adcontent.innerHTML = " <img class=x-pause-img width=" + this.info.VAL[0].W + " height=" + this.info.VAL[0].H + " src=" + this.info.VAL[0].RS + ">";
            this.adclose = this.adpause.getElementsByClassName("x-pause-close")[0];
            this.adimg = this.adcontent.getElementsByClassName("x-pause-img")[0];
            this.adimg.style.height = this.info.VAL[0].H + "px";
            this.adimg.style.width = this.info.VAL[0].W + "px";
            this.adpause.style.marginLeft = "-" + this.info.VAL[0].W / 2 + "px";
            this.adpause.style.marginTop = "-" + this.info.VAL[0].H / 2 + "px"
        },
        hide: function() {
            c.hide(this.adpause)
        },
        play: function() {
            2 != this.info.VAL[0].VT && (c.show(this.adpause), this._adreporter.sendSUS())
        },
        adClick: function() {
            window.open(this.info.VAL[0].CU, null);
            this._adreporter && this._adreporter.sendCUM()
        },
        loadVC: function() { (2 == this.info.VAL[0].VT || 1 == this.info.VAL[0].VT) && C(this.info.VAL[0].VC, "js")
        }
    };
    var za = function(b, c) {
        this._handler = {};
        this.player = b;
        this.video = this.player.video;
        this.controls = this.player.controls;
        this._adplugin = this.player._adplugin;
        this._adplugin.adplayer = this;
        this._addata = c.data.info;
        this.video.preload = "none";
        this.video.src = this._addata.VAL[0].RS;
        debug.log("ad src=" + this.video.src);
        this.video.style.display = "block";
        this._playTag = [];
        this.bindAdEvent();
        this._adreporter = new N(this, {
            curnum: 0,
            info: this._addata
        })
    };
    za.prototype = {
        addEventListener: function(b, c) {
            this._handler[b] = c
        },
        removeEventListener: function(b) {
            this._handler[b] = null
        },
        dispatch: function(b) {
            b && this._handler[b.type] && (b._target = this, this._handler[b.type](b))
        },
        bindAdEvent: function() {
            this.bind_fadtoplay = c.bindAsEventListener(this, this.onPlayClick);
            this.bind_fadplay = c.bindAsEventListener(this, this.onAdPlay);
            this.bind_fadended = c.bindAsEventListener(this, this.onAdEnded);
            this.bind_faderror = c.bindAsEventListener(this, this.onAdError);
            this.bind_fadpause = c.bindAsEventListener(this, this.onAdPause);
            this.bind_fadsuspend = c.bindAsEventListener(this, this.onAdSuspend);
            this.bind_fadstalled = c.bindAsEventListener(this, this.onAdStalled);
            this.bind_fadwaiting = c.bindAsEventListener(this, this.onAdWaiting);
            this.bind_fadloadedmetadata = c.bindAsEventListener(this, this.onAdLoadedMetaData);
            this.bind_fadtimeupdate = c.bindAsEventListener(this, this.onAdTimeUpdate);
            this.bind_fademptied = c.bindAsEventListener(this, this.onEmptied);
            c.addEventHandler(this.video, "play", this.bind_fadplay);
            c.addEventHandler(this.video, "error", this.bind_faderror);
            c.addEventHandler(this.video, "pause", this.bind_fadpause);
            c.addEventHandler(this.video, "suspend", this.bind_fadsuspend);
            c.addEventHandler(this.video, "stalled", this.bind_fadstalled);
            c.addEventHandler(this.video, "waiting", this.bind_fadwaiting);
            c.addEventHandler(this.video, "loadedmetadata", this.bind_fadloadedmetadata);
            c.addEventHandler(this.video, "timeupdate", this.bind_fadtimeupdate);
            c.addEventHandler(this.video, "emptied", this.bind_fademptied);
            this.shadow = this.controls.buttons.shadow;
            this.videobtn = this.controls.buttons.videobtn;
            c.addEventHandler(this.videobtn, "click", this.bind_fadtoplay, !0)
        },
        removeAdEvent: function() {
            c.removeEventHandler(this.video, "play", this.bind_fadplay);
            c.removeEventHandler(this.video, "ended", this.bind_fadended);
            c.removeEventHandler(this.video, "error", this.bind_faderror);
            c.removeEventHandler(this.video, "pause", this.bind_fadpause);
            c.removeEventHandler(this.video, "suspend", this.bind_fadsuspend);
            c.removeEventHandler(this.video, "stalled", this.bind_fadstalled);
            c.removeEventHandler(this.video, "waiting", this.bind_fadwaiting);
            c.removeEventHandler(this.video, "timeupdate", this.bind_fadtimeupdate);
            c.removeEventHandler(this.video, "loadedmetadata", this.bind_fadloadedmetadata);
            c.removeEventHandler(this.video, "loadedmetadata", this.bind_fademptied);
            c.removeEventHandler(this.videobtn, "click", this.bind_fadtoplay, !0)
        },
        onPlayClick: function() {
            this.video.play()
        },
        play: function() {
            this.video.load();
            this.video.play()
        },
        onEmptied: function() {
            this.checkPause()
        },
        leftSecond: function() {
            return parseInt(Math.max(0, this._addata.VAL[0].AL - this.video.currentTime))
        },
        clearTimer: function() {
            clearInterval(this._checkTimer);
            this._checkTimer = null
        },
        checkPause: function() {
            if (!this._checkTimer) {
                var b = this;
                this._timelist = [];
                this._checkTimer = setInterval(function() {
                    if (b.video.paused) b.onAdPause();
                    else b._timelist.push(b.video.currentTime),
                    3 <= b._timelist.length && (1 > Math.abs(b._timelist[0] - b._timelist[2]) && (debug.log("<b>ad unexpected pause</b>"), b.video.play(), 0 == b.leftSecond() && (debug.log("<b>exception left = 0 </b>"), b.onAdEnded())), b._timelist = [])
                },
                1E3)
            }
        },
        onAdPlay: function() {
            this.checkPause();
            var b = this.controls.container.poster;
            c.hide(this.controls.buttons.videobtn);
            c.hide(b);
            c.hide(c.get(".x-video-info"));
            this.video.style.display = "block";
            this._adplugin.setLeftSecond(this.leftSecond());
            var d = this;
            setTimeout(function() {
                debug.log("ad media timeout check begin = " + d._adBegin);
                d._adBegin || (d.removeAdEvent(), d._adplugin.hide(), d._adplugin.reportTime("advideo", -1, !1), d.dispatch({
                    type: z,
                    data: !0
                }))
            },
            15E3);
            this._playTag[0] || (this._playTag[0] = !0, this._adfirsttu = !1, this._adplugin.recordTime("advideo"), n.appendItem("phase", "adplay"))
        },
        uglyClose: function() {
            debug.log("united ugly close");
            this.onAdError()
        },
        onAdError: function() {
            this.removeAdEvent();
            this._adplugin.hide();
            this._adplugin.reportTime("advideo", -1, !1);
            this.clearTimer();
            this.dispatch({
                type: z,
                data: !0
            })
        },
        onAdEnded: function() {
            debug.log("united ad ended");
            this._adreporter.sendSUE();
            this.removeAdEvent();
            this._adplugin.hide();
            this.clearTimer();
            this.dispatch({
                type: B,
                data: !0
            });
            n.appendItem("phase", "adend")
        },
        onAdPause: function() {
            this.player.video.ended || (c.show(this.controls.buttons.videobtn), c.hide(this.controls.buttons.shadow))
        },
        onAdSuspend: function() {
            debug.log("<font color=red>ad suspend</font>")
        },
        onAdStalled: function() {
            debug.log("<font color=red>ad stalled</font>")
        },
        onAdWaiting: function(b) {
            this.controls.onWaiting(b)
        },
        onAdTimeUpdate: function() {
            if (this.video.currentTime > this._addata.VAL[0].AL) this.onAdEnded();
            else c.hide(this.controls.buttons.loading),
            this._adBegin = !0,
            c.hide(this.controls.buttons.loading),
            this._adplugin.setLeftSecond(this.leftSecond()),
            this._adreporter.sendSU(this.video.currentTime),
            this._adreporter.sendUnitedVTVC(this.video.currentTime),
            this._adfirsttu || (this._adplugin.show(), this._adreporter.sendSUS(), this._adfirsttu = !0, this._adplugin.reportTime("advideo"), 0 === this._adplugin.SKIP && this.dispatch({
                type: G
            }))
        },
        onAdLoadedMetaData: function() {
            this._adBegin = !0
        },
        onAdClick: function() {
            this.video.pause();
            this._adreporter.sendUnitedCUM(this.video.currentTime || 0);
            for (var b = this._addata.VAL[0].CU, c = this.video.currentTime, e = 0; e < b.length; e++) {
                var g = b[e],
                f = g.U;
                if (c <= parseInt(g.T)) {
                    window.open(f, "", "", !1);
                    break
                }
            }
        }
    };
    var da = function(b) {
        c.config = b;
        null == c.config.width && (c.config.width = p(c.config.parentBox).offsetWidth);
        this.buildDirectDom(p(c.config.parentBox))
    };
    da.prototype = {
        buildDirectDom: function(b) {
            b.innerHTML = "<div id=x-player class=" + D(c.config.width) + '><div class="x-video-poster"><img id="x-img"/></div><div class="x-video-button"><div class="x-video-play-ico"></div></div><div class="x-video-info"><h1 class="x-title"></h1><div class="x-video-state" style="display:none"><span class="x-time-span"></span></div><div class="x-showmore"></div><div class="x-mask"></div></div>'
        },
        bindEvent: function() {
            this._videobtn = c.get(".x-video-button");
            c.addEventHandler(this._videobtn, "click", c.bindAsEventListener(this, this.redirect))
        },
        startPlay: function(b, d) {
            c.v = b;
            c.videoInfo = d;
            c.videoInfo._playListData = b.data;
            this._pimg = c.get("#x-img");
            this._pimg.src = b.data.video.logo;
            this._title = c.get(".x-title");
            this._title.innerHTML = b.data.video.title;
            this._timespan = c.get(".x-time-span");
            this._timespan.innerHTML = c.getTime(b.data.video.seconds);
            c.show(c.get(".x-video-poster"));
            c.show(c.get(".x-video-info"));
            this.adapterForReport();
            this._reporter = new V(this, c.v, c.videoInfo._sid);
            this.bindEvent()
        },
        onPlayStart: function() {
            c.config.events && c.config.events.onPlayStart && (f.playerCurrentState = f.playerState.PLAYER_STATE_PLAYING, debug.log(f.playerCurrentState), debug.log("api:onplaystart"), c.config.events.onPlayStart())
        },
        getSrc: function() {
            if (this.src) return this.src;
            "m3u8" == c.config.content ? this.src = c.videoInfo.src: null != c.videoInfo._videoSegsDic && null != c.videoInfo._videoSegsDic[c.defaultVideoType] && (this.src = c.videoInfo._videoSegsDic[c.defaultVideoType][0].src);
            return this.src
        },
        redirect: function() {
            var b = this.getSrc();
            debug.log("redirect play src=" + b);
            f.isMIUI ? window.location.href = b: window.open(b, "", "", !1);
            this.onPlayStart();
            this._reporter.addPlayerStaticReport();
            this._reporter.addPlayerDurationReport(59);
            this._reporter.sendVVLog(59);
            this._reporter.sendTSLog(60);
            this._reporter.sendUserActionReport("xps", "c");
            this._reporter.sendThirdPartyReport("xplayer_dl");
            this._reporter.sendCustomLoadedTime(1);
            this._reporter.sendClientConsumeReport()
        },
        adapterForReport: function() {
            this.controls = {
                fullscreenPanel: {
                    fullFlag: function() {
                        return 1
                    }
                }
            };
            this.video = {
                src: this.getSrc()
            };
            this.getQuality = function() {
                return "m"
            }
        }
    }; (function(b) {
        b.getCurrAbsPath = function() {
            if (document.currentScript) return document.currentScript.src;
            var b;
            try {
                a.b.c()
            } catch(c) {
                b = c.fileName || c.sourceURL || c.stack || c.stacktrace,
                !b && window.opera && (b = (("" + c).match(/of linked script \S+/g) || []).join(" "))
            }
            if (b) return b = b.split(/[@ ]/g).pop(),
            b = "(" == b[0] ? b.slice(1, -1) : b,
            b.replace(/(:\d+)?:\d+$/i, "");
            b = -1 === ("" + document.querySelector).indexOf("[native code]");
            for (var g = document.scripts,
            f = g.length - 1,
            h; h = g[f--];) if ("interactive" === h.readyState) return b ? h.getAttribute("src", 4) : h.src
        }
    })(window);
    var ca = /(http|https|file):\/\/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/.exec(getCurrAbsPath())[0];
    C(ca + "/h5player/play.css?ver=" + "2015/11/2510:21:25".replace(/[-:]/g, ""), "css");
    var aa = function(b) {
        this._id = b.id;
        this._pid = b.pid || "";
        this._url = b.url;
        this._box = b.parentBox;
        this._gotInfo = !1;
        b.width = p(b.parentBox).offsetWidth;
        b.height = p(b.parentBox).offsetHeight;
        c.config = b;
        this.request()
    };
    aa.prototype = {
        request: function() {
            window.pkinfo = this;
            A(this._url + "/h5/videos/play.json?vid=" + this._id + "&pid=" + this._pid + "&callback=pkinfo.parse");
            var b = this;
            setTimeout(function() { ! 0 != b._gotInfo && b.showError()
            },
            5E3)
        },
        parse: function(b) {
            this._gotInfo = !0;
            0 == b.error ? (this.videoSrc = b.results.url, this.imgSrc = b.results.cover, this.buildDom()) : this.showError()
        },
        buildDom: function() {
            var b = "<div id=x-player class=" + this.cssAdapt(parseInt(c.config.width)) + ">";
            this.$(this._box).innerHTML = b + "<video class=x-video-player id=youku-html5player-video style=width: 100%; height: 100%; position: relative; display: none; top: -1000px; src=" + this.videoSrc + "></video><div class=x-video-poster><img src=" + this.imgSrc + "></img></div><div class=x-video-loading></div><div id=x-video-button class=x-video-button><div class=x-video-play-ico></div></div></div>";
            this.video = c.get(".x-video-player");
            this.cover = c.get(".x-video-poster");
            this.videoBtn = c.get(".x-video-button");
            this.loading = c.get(".x-video-loading");
            c.addEventHandler(this.videoBtn, "click", c.bindAsEventListener(this, this.onOverBtnClick));
            c.addEventHandler(this.video, "ended", c.bindAsEventListener(this, this.onEnded));
            c.addEventHandler(this.video, "timeupdate", c.bindAsEventListener(this, this.onTimeUpdate));
            c.addEventHandler(this.video, "waiting", c.bindAsEventListener(this, this.onWaiting))
        },
        showError: function() {
            this.$(this._box).innerHTML = '<div style="background:#000; color:#FFF; text-align:center; color: white; line-height:' + document.getElementById(this._box).offsetHeight + 'px " >\u89c6\u9891\u4fe1\u606f\u51fa\u9519 <a href="http://m.youku.com/webapp/dl?app=youku&amp;source=webqr" title="\u4e0b\u8f7d\u4f18\u9177\u5ba2\u6237\u7aef" target="_blank"><button type="button" class="x-btn" style="background: #3bb4fc;text-align: center;color: #fff;border-radius: 1rem;">\u7528app\u89c2\u770b</button></a></div>'
        },
        onOverBtnClick: function() {
            this.video.play();
            this.loading.style.display = "block";
            this.videoBtn.style.display = "none"
        },
        onEnded: function() {
            this.cover.style.display = "block";
            this.videoBtn.style.display = "block";
            this.loading.style.display = "none";
            this.video.style.display = "none"
        },
        onTimeUpdate: function() {
            "none" != this.loading.style.display && (this.loading.style.display = "none");
            "block" != this.video.style.display && (this.video.style.display = "block");
            "none" != this.cover.style.display && (this.cover.style.display = "none")
        },
        onWaiting: function() {
            this.loading.style.display = "block"
        },
        cssAdapt: function(b) {
            return f.isIPAD && 0 <= window.location.href.indexOf("v.youku.com") ? "x-player": 200 >= b ? "x-player x-player-200": 300 >= b ? "x-player x-player-200-300": 660 >= b ? "x-player x-player-300-660": 800 >= b ? "x-player x-player-660-800": "x-player"
        },
        $: function(b) {
            return document.getElementById(b)
        }
    };
    var Aa = function(b, d) {
        this.setting = {
            debug: !1,
            controls: c.get(".x-console"),
            feedback: c.get(".x-feedback"),
            container: {
                poster: c.get(".x-video-poster")
            },
            buttons: {
                pointVideo: c.get("#point-video"),
                playControl: c.get(".x-play-control"),
                play: c.get("#x-playbtn"),
                videobtn: c.get(".x-video-button"),
                loading: c.get(".x-video-loading"),
                videoinfo: c.get(".x-video-info"),
                shadow: c.get(".x-trigger"),
                currentTime: c.get(".x-time-current"),
                totalTime: c.get(".x-time-duration"),
                fullscreen: c.get(".x-fullscreen")
            },
            classNames: {
                play: "x-playing",
                pause: "x-pause"
            },
            init: function() {}
        };
        c.extend(this.setting, d);
        this.player = b;
        this.dashboard = this.setting.controls;
        this.container = this.setting.container;
        this.progressBar = new qa(b);
        this.progressBar.uCurrentTime = this.setting.buttons.currentTime;
        this.miniProgressBar = new ma(b);
        this.fullscreenPanel = new ia(b);
        this.interactionPanel = new ka(b);
        this.xplayer = c.get("#x-player");
        this.buttons = this.setting.buttons
    };
    Aa.prototype = {
        init: function(b, d) {
            this.buttons.totalTime.innerHTML = d.totalTime ? c.getTime(d.totalTime) : "00:00";
            this.resetProgress();
            this.buttons.play.className = this.setting.classNames.play;
            var e = this.container.poster.getElementsByTagName("img")[0];
            c.config.poster ? e.src = c.config.poster: b.data.trial && "episodes" != b.data.trial.type || b.data.error ? null != b.data.error && -203 == b.data.error.code && (this.container.poster.style.backgroundColor = "black", e.parentNode.removeChild(e), c.show(this.container.poster)) : (e.src = b.data.video.logo, this.container.poster.style.display = "block");
            this._qualityPanel = new ta(this.player, b);
            this._languagePanel = new la(this.player, b);
            this._playratePanel = new pa(this.player, b);
            this._payPanel = new na(this.player, b);
            this._feedbackPanel = new U(this.player, b);
            this._informationPanel = new ja(this.player, b);
            this.tipPanel = new wa(this.player, b);
            this.showlistPanel = new va(this.player, b);
            this.playLimit = new oa(this.player, b);
            this.bindDynamicEvent()
        },
        bindDynamicEvent: function() {
            this.bind_mutualHide = c.bindAsEventListener(this, this.mutualHide);
            c.addEventHandler(this._languagePanel, "click", this.bind_mutualHide);
            c.addEventHandler(this._qualityPanel, "click", this.bind_mutualHide);
            c.addEventHandler(this.showlistPanel, "click", this.bind_mutualHide);
            c.addEventHandler(this._playratePanel, "click", this.bind_mutualHide);
            this.bind_progress = c.bindAsEventListener(this, this.onProgress);
            c.addEventHandler(this.progressBar, "progressing", this.bind_progress);
            c.addEventHandler(this.progressBar, "progressend", c.bindAsEventListener(this, this.onProgressEnd));
            c.addEventHandler(this._languagePanel, "settingdone", c.bindAsEventListener(this, this.onSettingDone));
            c.addEventHandler(this._qualityPanel, "settingdone", c.bindAsEventListener(this, this.onSettingDone));
            c.addEventHandler(this._playratePanel, "settingdone", c.bindAsEventListener(this, this.onSettingDone));
            c.addEventHandler(this._languagePanel, "settingshow", c.bindAsEventListener(this, this.onSettingShow));
            c.addEventHandler(this._qualityPanel, "settingshow", c.bindAsEventListener(this, this.onSettingShow));
            c.addEventHandler(this._playratePanel, "settingshow", c.bindAsEventListener(this, this.onSettingShow));
            c.addEventHandler(this._languagePanel, "settinghide", c.bindAsEventListener(this, this.onSettingHide));
            c.addEventHandler(this._qualityPanel, "settinghide", c.bindAsEventListener(this, this.onSettingHide));
            c.addEventHandler(this._playratePanel, "settinghide", c.bindAsEventListener(this, this.onSettingHide));
            c.addEventHandler(this.fullscreenPanel, "enterfullscreen", c.bindAsEventListener(this, this.onEnterFullScreen));
            c.addEventHandler(this.fullscreenPanel, "exitfullscreen", c.bindAsEventListener(this, this.onExitFullScreen))
        },
        retimer: function() {
            debug.log("retimer");
            this.autoHideDashBoard()
        },
        hideDashBoard: function() {
            var b = this._payPanel,
            c = this._informationPanel,
            e = this.miniProgressBar,
            g = this.interactionPanel,
            f = this._languagePanel;
            this.setting.controls.style.display = "none";
            e.show();
            b.hide();
            c.hide();
            g.hideStatus();
            f.hide();
            this._qualityPanel.hide();
            this._playratePanel.hide()
        },
        autoHideDashBoard: function(b) {
            this.dashboardTimer && clearTimeout(this.dashboardTimer);
            var d = this;
            this.dashboardTimer = setTimeout(function() {
                var e = c.get(".x-showlist");
                e && "block" == e.style.display ? d.autoHideDashBoard(b) : d.player.video.paused || d.hideDashBoard()
            },
            b || 2E3)
        },
        onMultiTouch: function() {},
        showUglyHint: function() {},
        closeUglyHint: function() {},
        showBoardInfo: function() {
            c.show(this.setting.controls);
            this.miniProgressBar.hide();
            this._informationPanel.show();
            this._payPanel.hasPayInfo() && this._payPanel.show()
        },
        toggleDashBoard: function(b) {
            if (! ("touchend" == b.type && 1 < b.changedTouches.length)) {
                this._sx = this._sx || 0;
                this._sy = this._sy || 0;
                b.changedTouches = b.changedTouches || [{
                    clientX: this._sx,
                    clientY: this._sy
                }];
                var c = {
                    x: this._sx,
                    y: this._sy
                },
                b = {
                    x: b.changedTouches[0].clientX,
                    y: b.changedTouches[0].clientY
                }; ! this._stmtag && (1 !== this._sactionType && this.isTouchTooShort(c, b, 100)) && (c = this.setting.controls.style.display, "none" == c || "" == c ? (this.player._reporter.sendUserActionReport("xcd", "c"), this.showBoardInfo(), this.autoHideDashBoard(), ra = (new Date).getTime()) : (this.player._reporter.sendUserActionReport("xhd", "c"), clearTimeout(this.dashboardTimer), this.hideDashBoard()))
            }
        },
        bindAdVideoBtnEvent: function() {
            c.addEventHandler(this.buttons.videobtn, "touchstart", c.bindAsEventListener(this, this.onVideoBtnTouchStart));
            c.addEventHandler(this.buttons.videobtn, "touchend", c.bindAsEventListener(this, this.onVideoBtnTouchEnd))
        },
        bindVideoBtnEvent: function() {
            c.addEventHandler(this.buttons.videobtn, "click", c.bindAsEventListener(this, this.onVideoBtnClick), !0)
        },
        bindEvent: function() {
            debug.log("bind event");
            this.bind_uireinit = c.bindAsEventListener(this, this.uiInit);
            this.bind_play = c.bindAsEventListener(this, this.play);
            this.bind_redirect = c.bindAsEventListener(this, this.redirect);
            this.bind_showTimeTip = c.bindAsEventListener(this, this.showTimeTip);
            this.bind_hideTimeTip = c.bindAsEventListener(this, this.hideTimeTip);
            this.bind_changeVolume = c.bindAsEventListener(this, this.changeVolume);
            this.bind_toggleVolume = c.bindAsEventListener(this, this.toggleVolume);
            this.bind_gestureChange = c.bindAsEventListener(this, this.onGestureChange);
            this.bind_toggleDashBoard = c.bindAsEventListener(this, this.toggleDashBoard);
            this.bind_retimer = c.bindAsEventListener(this, this.retimer);
            c.addEventHandler(this.progressBar, "click", this.bind_uireinit);
            c.addEventHandler(this.setting.controls, "click", this.bind_retimer);
            c.addEventHandler(this.setting.controls, "touchstart", this.bind_retimer);
            c.addEventHandler(this.buttons.playControl, "click", this.bind_play);
            "directsrc" == c.config.playType && (!f.isIPHONE && !f.isIPOD ? c.addEventHandler(this.buttons.videobtn, "click", this.bind_redirect, !0) : c.addEventHandler(this.buttons.videobtn, "click", c.bindAsEventListener(this, this.playIPH), !0));
            c.addEventHandler(this.buttons.shadow, "touchstart", c.bindAsEventListener(this, this.shadowTouchStart));
            c.addEventHandler(this.buttons.shadow, "touchmove", c.bindAsEventListener(this, this.shadowTouchMove));
            c.addEventHandler(this.buttons.shadow, "touchend", c.bindAsEventListener(this, this.shadowTouchEnd));
            c.addEventHandler(this.buttons.shadow, "click", this.bind_toggleDashBoard);
            c.addEventHandler(this.buttons.shadow, "touchend", c.bindAsEventListener(this, this.onMultiTouch));
            c.addEventHandler(this.buttons.shadow, "gesturechange", this.bind_gestureChange)
        },
        removeEvent: function() {
            debug.log("remove event begin");
            c.removeEventHandler(this.progressBar, "click", this.bind_uireinit);
            c.removeEventHandler(this.buttons.playControl, "click", this.bind_play);
            c.removeEventHandler(this.buttons.shadow, "click", this.bind_toggleDashBoard);
            c.removeEventHandler(this.progressBar, "touchstart", this.bind_uireinit);
            c.removeEventHandler(this._languagePanel, "click", this.bind_mutualHide);
            c.removeEventHandler(this._qualityPanel, "click", this.bind_mutualHide);
            c.removeEventHandler(this._playratePanel, "click", this.bind_mutualHide);
            this.progressBar.removeEvent();
            this.fullscreenPanel.removeEvent();
            this._languagePanel.removeEvent();
            this._qualityPanel.removeEvent();
            debug.log("remove event end")
        },
        onGestureChange: function(b) {
            b.preventDefault();
            var c = -1 !== this.fullscreenPanel.zoomStatus().indexOf("in");
            if (1.1 < b.scale && c || 0.9 > b.scale && !c) b.method = "m",
            this.fullscreenPanel.switchFullScreen(b)
        },
        toggleVolume: function() {},
        changeVolume: function() {},
        rePlay: function() {
            debug.log("replay");
            this.player._reporter.sendUserActionReport("xrp", "c");
            y = !1; (this._recommend = c.get(".x-recommend")) && c.get("#x-player").removeChild(this._recommend);
            this.resetProgress();
            this._first = !1;
            this.player.replay();
            debug.log("replay func end")
        },
        redirect: function(b) {
            this.player.redirect(b)
        },
        hideFacade: function() {
            var b = this.container.poster;
            c.hide(this.buttons.videobtn);
            c.hide(b);
            c.hide(c.get(".x-feedback"));
            debug.log("<font color=blue>hide facade</font>")
        },
        onVideoBtnTouchStart: function(b) {
            this._vtsx = b.targetTouches[0].clientX;
            this._vtsy = b.targetTouches[0].clientY
        },
        onVideoBtnTouchEnd: function(b) {
            debug.log("<font color=red>video btn clicked</font>");
            b = b || {};
            y ? this.rePlay() : b && b.changedTouches && 50 < Math.abs(b.changedTouches[0].clientY - this._vtsy) ? debug.log("videobtn too long y") : (this.player._reporter.sendUserActionReport("xps", "c"), !0 !== this._hasAdReq && (this._hasAdReq = !0, this.hideFacade(), debug.log("active src=" + this.player.video.src), this.player.video.load(), this.player.requestAd()))
        },
        onVideoBtnClick: function() {
            if ((f.isIPHONE || f.isIPOD) && null != c.v.data.trial) this.player.video.style.display = "block";
            if (y) this.rePlay();
            else if (!c.v.data.trial || !("episodes" != c.v.data.trial.type && 0 == c.v.data.trial.time)) this.player.video.load(),
            this.player.video.play()
        },
        playIPH: function() {
            if (!this.iphTag) {
                this.player.video.load();
                var b = this;
                this.player.video.addEventListener("timeupdate",
                function(c) {
                    4 == c.target.readyState && (b.iphTag = !0)
                })
            }
            this.player.video.play()
        },
        play: function(b) {
            b = b || {};
            if (y) this.rePlay();
            else {
                var c = this.player.video.paused;
                debug.log("m3u8 isPause = " + c + " e = " + b);
                c ? (0 === this._payPanel.activeTime ? (this._payPanel.activeTime = -1, this.player.seek(0)) : this.player.video.play(), this.player._reporter.sendUserActionReport("xpl", "c"), this.interactionPanel.setStatus("\u64ad\u653e")) : (this.player.video.pause(), this.player._reporter.sendUserActionReport("xpa", "c"), this.interactionPanel.setStatus("\u6682\u505c"));
                this.checkPauseAd()
            }
        },
        isProperWH: function(b, d) {
            var e = c.get("#x-player");
            return e.offsetWidth >= b && e.offsetHeight >= d
        },
        isNeedPauseAd: function() {
            return this.player.video.paused && c.isLandScape()
        },
        checkPauseAd: function() {
            this.isNeedPauseAd() ? (this._pauseAdPlugin = new X(this.player, c.v, c.videoInfo._sid), this._pauseAdPlugin.addEventListener("pauseAdinfook", c.bindAsEventListener(this, this.onPauseAdInfoOK)), this._pauseAdPlugin.addEventListener("pauseadinfotimeout", c.bindAsEventListener(this, this.onPauseAdInfoTimeout)), this._pauseAdPlugin.addEventListener("pauseAdinfoerror", c.bindAsEventListener(this, this.onPauseAdInfoERROR)), window.adpluginobject = this._pauseAdPlugin, this._pauseAdPlugin.pauseAd(), debug.log("send pause ad request<br/>")) : (debug.log("<font color=blue> donot need pause ad </font>"), this.hidePauseAd())
        },
        hidePauseAd: function() {
            c.hide(c.get(".x-ad-pause"))
        },
        onPauseAdInfoOK: function(b) {
            debug.log("pause info ok");
            this._pauseAdStart || (this._pauseAdStart = !0);
            this._pauseAdPlayer = new ya(this.player, b);
            this._pauseAdPlayer.play()
        },
        onPauseAdInfoTimeout: function(b) {
            debug.log("pause info timeout = " + b.data.timeout);
            this._pauseAdStart || (this._pauseAdStart = !0)
        },
        onPauseAdInfoERROR: function() {
            debug.log("<font color=blue>pause info error no info</font>");
            this._pauseAdStart || (this._pauseAdStart = !0)
        },
        autoShow: function() {
            this.show();
            var b = this;
            setTimeout(function() {
                b.hide()
            },
            5E3)
        },
        mutualHide: function(b) {
            b._target == this._languagePanel ? (this._qualityPanel.hide(!0), this._playratePanel.hide(!0), this.showlistPanel.hide()) : b._target == this._qualityPanel ? (this._languagePanel.hide(!0), this._playratePanel.hide(!0), this.showlistPanel.hide()) : b._target == this.showlistPanel ? (this._qualityPanel.hide(!0), this._languagePanel.hide(!0), this._playratePanel.hide(!0)) : b._target == this._playratePanel && (this._qualityPanel.hide(!0), this._languagePanel.hide(!0), this.showlistPanel.hide())
        },
        show: function(b) {
            b ? c.show(this.buttons[b]) : c.show(this.setting.controls)
        },
        hide: function(b) {
            b ? c.hide(this.buttons[b]) : c.hide(this.setting.controls)
        },
        backAdPrepare: function() {
            this.dashboard.style.display = "none";
            this.buttons.shadow.display = "none"
        },
        onEnded: function() {
            this.dashboard.style.display = "none";
            this.buttons.shadow.display = "none";
            this.buttons.videobtn.style.display = "block";
            this.container.poster.style.display = "block";
            this._informationPanel.show();
            this.miniProgressBar.hide();
            this.interactionPanel.hide();
            null == c.v.data.trial && !1 != c.initConfig.show_related && (this._relatedPanel = new ua(this.player, c.v))
        },
        onPlay: function() {
            this.player.video.style.display = "block";
            this.buttons.play.className = this.setting.classNames.pause;
            this.buttons.videobtn.style.display = "none";
            this.container.poster.style.display = "none";
            this.hidePauseAd();
            this.buttons.shadow.style.display = "block"; (this._recommend = c.get(".x-recommend")) && c.get("#x-player").removeChild(this._recommend);
            y = !1;
            this._first || (this._first = !0, this._informationPanel.show(), this.setting.controls.style.display = "block");
            this.autoHideDashBoard(5E3)
        },
        onPause: function() {
            this.buttons.play.className = this.setting.classNames.play;
            c.hide(this.buttons.loading);
            this.interactionPanel.isVisible() || (this.showBoardInfo(), this.interactionPanel.setStatus("\u6682\u505c"))
        },
        onWaiting: function() { ! this.player.video.paused && "none" == this.buttons.videobtn.style.display && (this.buttons.loading.style.display = "block")
        },
        onTryPlayEnded: function() {
            debug.log("try end");
            var b = this.player.video;
            this.player.video.pause();
            this._payPanel.activeTime = 0;
            y = !0;
            this.onEnded({
                target: b
            });
            this._payPanel.showTip();
            var c = this;
            setTimeout(function() {
                c.dashboard.style.display = "none";
                c.buttons.shadow.style.display = "none";
                c.interactionPanel.hide()
            },
            1E3)
        },
        onTimeUpdate: function(b) {
            this.buttons.loading.style.display = "none";
            if (b.target == this.player.video) {
                var c = this.player.currentTime;
                4 == b.target.readyState && this.setProgress(c);
                if (this._payPanel.hasPayInfo() && c >= this._payPanel.tryDuration()) this.onTryPlayEnded();
                this.playLimit.isLimit() && c >= this.playLimit.limitTime() && this.playLimit.create()
            }
        },
        checkPlayLimit: function() {
            var b = !1;
            c.v.data.trial ? b = this.player.currentTime >= c.v.data.trial.time / 100 : this.playLimit.isLimit() && (b = this.player.currentTime >= this.playLimit.limitTime());
            if (!b) return ! 1;
            this.playLimit.create();
            return ! 0
        },
        removeControls: function() {
            this.video.controls = !1
        },
        loadControls: function() {
            this.video.controls = !0
        },
        setProgress: function(b) {
            b = Math.min(Math.max(b, 0), c.videoInfo.totalTime);
            this.progressBar.setProgress(b);
            this.miniProgressBar.setProgress(b);
            this.buttons.currentTime.innerHTML = c.getTime(this.progressBar.playTime)
        },
        resetProgress: function() {
            this.progressBar.resetProgress();
            this.miniProgressBar.resetProgress();
            this.buttons.currentTime.innerHTML = "00:00"
        },
        hideTimeTip: function(b) {
            if (b.srcElement.id == this.buttons.progressHandler.id) return ! 1;
            this.buttons.progressTime.style.display = "none"
        },
        showTimeTip: function(b) {
            if (b.srcElement.id == this.buttons.progressHandler.id || b.srcElement.id == this.buttons.progressTime.id || b.srcElement.id == this.buttons.pointVideo.id) return ! 1;
            b = b.offsetX / this.buttons.progressBar.offsetWidth;
            this.buttons.progressTime.innerHTML = c.getTime(b * c.videoInfo.totalTime);
            this.buttons.progressTime.style.left = 100 * Math.min(Math.max(b, 0.023), 0.977) + "%";
            this.buttons.progressTime.style.display = "block"
        },
        shadowTouchStart: function(b) {
            1 < b.targetTouches.length ? this.interactionPanel.hide() : (this._sx = b.targetTouches[0].clientX, this._sy = b.targetTouches[0].clientY, this._smx = this._sx, this._smy = this._sy, this._presmx = this._sx, this._presmy = this._sy, this._deltaxs = [], this._ttime = this._stime = this.player.currentTime || 0, this._spretag = this._stmtag = !1, this._presmt = this._sactionTime = (new Date).getTime(), this._stmlrtag = this._sactionType = 0)
        },
        shadowTouchMove: function(b) {
            if (1 < b.targetTouches.length) this.interactionPanel.hide();
            else {
                this._smx = b.targetTouches[0].clientX;
                this._smy = b.targetTouches[0].clientY;
                this._smt = (new Date).getTime();
                var c = Math.abs(this._smx - this._sx),
                e = Math.abs(this._smy - this._sy),
                g = this._smt - this._sactionTime;
                0 === this._stmlrtag && (this._stmlrtag = c > e ? 1 : -1);
                1 == this._stmlrtag && b.preventDefault();
                if (1 != this._sactionType) if (100 < c && c > e && 500 > g) debug.log("quick seek moving"),
                this.player.video.pause(),
                this._sactionType = 1,
                g = this._smx > this._sx ? 30 : -30,
                this.interactionPanel.setTip(this._stime, g),
                this.interactionPanel.show();
                else if (200 > c && (100 > e && 1E3 < g) && (this._spretag = !0), this._spretag && c > e || this._stmtag) debug.log("stmtag =" + this._stmtag),
                this._sactionType = 2,
                this._stmtag = !0,
                this.player.video.pause(),
                this.dragging(b)
            }
        },
        shadowTouchEnd: function(b) {
            1 < b.changedTouches.length ? this.interactionPanel.hide() : (this.adrAdapt(b), this.isShadowTouchTooShort() && !this._stmtag && 1 != this._sactionType ? debug.log("too short or horizontal") : (b = Math.abs(this._smy - this._sy) > Math.abs(this._smx - this._sx) ? "xdud": "xdlr", debug.log("shadow action = " + b), this.player._reporter.sendUserActionReport(b, "d"), 2 == this._sactionType ? (debug.log("<br/><b>normal seek</b>"), this.player.video.play(), this.player.seek(this._ttime), this.interactionPanel.hide(), this.player._reporter.sendUserActionReport("xtseek", "d"), f.Log(f.uniplayerUrl + u({
                e: "xtseek",
                adr: f.isAndroid,
                ios: f.isIPAD,
                d: parseInt(this._ttime - this._stime)
            }))) : 1 == this._sactionType && (b = 0 < this._smx - this._sx ? 30 : -30, debug.log("<br/><font color=red>quick seek deltat = " + b + " cur=" + this._stime + "</font>"), this.setProgress(this._stime + b), this.interactionPanel.setTip(this._stime, b), this.interactionPanel.show(), this.interactionPanel.autoHide(), this.player.video.play(), this.player.seek(this._stime + b), this.player._reporter.sendUserActionReport("xqseek", "d"), f.Log(f.uniplayerUrl + u({
                e: "xqseek",
                adr: f.isAndroid,
                ios: f.isIPAD,
                d: b
            })), debug.log("<br/>"))))
        },
        dragging_: function(b) {
            var d = this._smx - this._presmx;
            this._deltaxs.push(10 < d ? d / 2 : d);
            for (var e = d = 0; e < this._deltaxs.length; e++) d += this._deltaxs[e];
            b = Math.min(Math.max(d / b.currentTarget.offsetWidth * c.videoInfo.totalTime + this._stime, 0), c.videoInfo.totalTime);
            this.setProgress(b);
            this.interactionPanel.show();
            this._ttime = b;
            this._presmx = this._smx;
            this._presmy = this._smy;
            this._presmt = this._smt
        },
        dragging: function(b) {
            b = Math.min(Math.max(60 * ((this._smx - this._sx) / b.currentTarget.offsetWidth) + this._stime, 0), c.videoInfo.totalTime);
            this.setProgress(b);
            this.interactionPanel.setTip(this._ttime, b - this._ttime);
            this.interactionPanel.show();
            this._ttime = b;
            this._presmx = this._smx;
            this._presmy = this._smy;
            this._presmt = this._smt
        },
        onProgress: function(b) {
            this.interactionPanel.setTip(b.st || 0, b.dt || 0);
            this.interactionPanel.show()
        },
        onProgressEnd: function() {
            this.interactionPanel.hide()
        },
        onSettingDone: function() {
            this.interactionPanel.setStatus("\u8bbe\u7f6e\u6210\u529f")
        },
        onSettingShow: function() {
            debug.log("<b>setting show</b>");
            clearTimeout(this.pbarClickTimer);
            this.progressBar.removeClickEvent()
        },
        onSettingHide: function() {
            debug.log("<b>setting hide</b>");
            var b = this;
            this.pbarClickTimer = setTimeout(function() {
                b.progressBar.addClickEvent()
            },
            1E3)
        },
        onEnterFullScreen: function() {
            f.isIPAD && c.addClass(this.setting.controls, "x-fs-console")
        },
        onExitFullScreen: function() {
            f.isIPAD && c.removeClass(this.setting.controls, "x-fs-console")
        },
        adrAdapt: function(b) {
            f.isAndroid && (this._smx = b.changedTouches[0].clientX, this._smy = b.changedTouches[0].clientY, debug.log("<hr/>adr smy= " + this._smy + " y = " + this._sy))
        },
        isShadowTouchTooShort: function(b) {
            return this.isTouchTooShort({
                x: this._sx,
                y: this._sy
            },
            {
                x: this._smx,
                y: this._smy
            },
            b)
        },
        isTouchTooShort: function(b, c, e) {
            var g = Math.abs(c.x - b.x),
            g = g || 1.0E-6,
            b = (b = Math.abs(c.y - b.y)) || 1.0E-6;
            debug.log(g + "," + b);
            e = e || 100;
            return g < e && b < e ? !0 : !1
        },
        showShowListBtn: function() {
            this.showlistPanel.showListBtn()
        },
        hideShowListBtn: function() {
            this.showlistPanel.hideListBtn()
        },
        showLastTimeTip: function(b) {
            0 >= b || this.tipPanel.showLastTimeTip(b)
        },
        uiInit: function() {
            debug.log("uiInit");
            y && (y = !1, this.buttons.videobtn.style.display = "block")
        },
        onResize: function(b) {
            var d = p(c.config.parentBox).offsetWidth,
            e = p(c.config.parentBox).offsetHeight;
            if (d && (e && c.resizeTag) && (e = this.xplayer.className, this.xplayer && ( - 1 === e.indexOf("fullscreen") ? this.xplayer.className = D(d) : (d = window.innerWidth, this.xplayer.className = D(d) + " x-player-fullscreen")), this._relatedPanel)) this._relatedPanel.onResize(b)
        }
    };
    var Y = function() {
        this.video = c.get("#youku-html5player-video");
        this._startPlayTime = -1;
        this.currentTime = this._waitTry = 0
    };
    Y.prototype = {
        getVideo: function() {
            return this.video
        },
        show: function() {
            c.show(this.video)
        },
        hide: function() {
            c.hide(this.video)
        },
        play: function() {
            c.v && c.v.data.trial && 0 == c.v.data.trial.time ? debug.log("<b> trial time = 0  </b>") : this.video.play()
        },
        pause: function() {
            this.video.pause()
        },
        setupControls: function(b) {
            this.controls && this.controls.removeEvent();
            return new Aa(b)
        },
        hideControls: function() {
            this.controls.hide()
        },
        showControls: function() {
            this.controls.show()
        },
        removeControls: function() {
            this.controls.removeControls()
        },
        loadControls: function() {
            this.controls.loadControls()
        },
        retry: function() {},
        showError: function(b) {
            this.errorBox || (this.errorBox = document.createElement("div"), this.errorBox.style.cssText = "position:absolute;width:100%;top:50%;display:none;text-align:center;", this.video.parentNode.appendChild(this.errorBox));
            this.errorBox.innerHTML = b;
            this.errorBox.style.marginTop = "-" + this.errorBox.offsetHeight / 2 + "px";
            this.errorBox.style.display = "block"
        },
        onLoadStart: function() {},
        onCanPlay: function() {},
        onLoadedData: function() {},
        onLoadedMetaData: function() {},
        onAbort: function() {},
        onError: function() {
            this._reporter.sendUserActionReport("xve", "e");
            this._reporter.sendUepReport("videoload", -1, !1);
            f.uniReport({
                error: 10,
                vid: c.v.data.id,
                time: this.currentTime,
                errorcode: this.video.error.code,
                ua: encodeURI(navigator.userAgent.replace(/[\/\+\*@\(\)\,]/g, ""))
            });
            f.sendErrorReport(2001);
            if (0 <= this._retry--) - 1 !== this.video.src.indexOf("m3u8") && (this.video.src = c.m3u8src_v2(c.v.data.id, c.defaultVideoType)),
            debug.log("video onerror retry it ,time=" + this.currentTime + " src=" + this.video.src),
            this.video.load(),
            this.video.play(),
            this.seek(this.currentTime);
            else if (! (this.isOnePiece() && !0 == this.controls.checkPlayLimit()) && !this._errorTag) {
                f.uniReport({
                    error: 11,
                    errorcode: this.video.error.code,
                    vid: c.v.data.id,
                    ua: encodeURI(navigator.userAgent.replace(/[\/\+\*@\(\)\,]/g, ""))
                });
                this._errorTag = !0;
                if (c.playerEvents && c.playerEvents.onPlayError) c.playerEvents.onPlayError("\u62b1\u6b49\uff0c\u89c6\u9891\u51fa\u9519\uff0c\u8bf7\u5237\u65b0");
                var b = c.get("#x-player");
                b.innerHTML = "\u62b1\u6b49\uff0c\u89c6\u9891\u51fa\u9519\uff0c\u8bf7\u5237\u65b0";
                b.style.textAlign = "center";
                b.style.color = "white";
                b.style.lineHeight = b.offsetHeight + "px"
            }
        },
        onPause: function() {
            this.controls.onPause()
        },
        onPlayIPH: function() {
            debug.log("onplayiph");
            this.onPlayStart();
            this._firstPlayTag ? !0 == this._endedIPH && (this._reporter.tsInit(), this._reporter.sendVVLog(62), this._reporter.sendTSLog(60), this._reporter.addPlayerDurationReport(62)) : (this._firstPlayTag = !0, this._reporter.addPlayerStaticReport(), this._reporter.addPlayerDurationReport(59), this._reporter.sendVVLog(59), this._reporter.sendTSLog(60), this._reporter.sendUserActionReport("xps", "c"), this._reporter.sendLoadedTime(3), this._reporter.sendThirdPartyReport("xplayer_iph"), this._reporter.sendClientConsumeReport())
        },
        onTimeUpdateIPH: function() {
            this.currentTime = this.video.currentTime
        },
        onEndedIPH: function() {
            this.onPlayEnd();
            this._reporter.addPlayerDurationReport(61);
            this._reporter.sendTSLog(61);
            this._endedIPH = !0
        },
        onPlay: function() {
            debug.log("onplay");
            this.controls.onPlay();
            this._firstPlayTag || (this._firstPlayTag = !0, this.onPlayStart(), c.initConfig.firsttime ? (debug.log("starttime = " + c.initConfig.firsttime), this.seek(c.initConfig.firsttime)) : this.seekToLastPoint() || this.skipHead(), this._startPlayTime = (new Date).getTime(), this._reporter.addPlayerStaticReport(), this._reporter.addPlayerDurationReport(59), this._reporter.sendVVLog(59), this._reporter.sendTSLog(60), this._reporter.sendClientConsumeReport());
            n.appendItem("phase", "videoplay")
        },
        onVolumeChange: function() {},
        onPlaying: function() {},
        onStalled: function(b) {
            debug.log("<b>stalled</b>");
            if (this.isOnePiece() || b.target == this.video) this.controls.onWaiting(b)
        },
        onSuspend: function() {},
        onWaiting: function(b) {
            if (this.isOnePiece() || b.target == this.video) this.controls.onWaiting(b)
        },
        onSeeked: function() {
            debug.log("onSeeked waitSkip=" + this._waitSeek + " try= " + this._waitTry);
            if (!isNaN(this._waitSeek)) {
                var b = this._waitSeek;
                10 < Math.abs(this.video.currentTime - b) && 5 >= this._waitTry ? (this._waitTry += 1, this.seek(b)) : this._waitSeek = "NaN"
            }
        },
        onSeeking: function(b) {
            debug.log("seeking");
            if (this.isOnePiece() || b.target == this.video) {
                var c = this;
                setTimeout(function() {
                    c.controls.onWaiting(b)
                },
                100)
            }
        },
        onDurationChange: function() {},
        onProgress: function() {},
        onRateChange: function() {},
        customWaiting: function() {
            var b = this; ! 1 == this.video.paused && this._lastTime === this.currentTime && (debug.log("custom waiting!:) networkstate=" + this.video.networkState), this.controls.onWaiting());
            this._lastTime = this.currentTime;
            setTimeout(function() {
                b.customWaiting()
            },
            5E3)
        },
        sendLoadedTime: function() {
            var b = 0,
            b = -1 == this._startPlayTime ? 0 : (new Date).getTime() - this._startPlayTime;
            this._reporter.sendLoadedTime(b)
        },
        onTimeUpdate: function(b) {
            if (this.isOnePiece()) this.currentTime = this.video.currentTime,
            c.unitedTag && (this.currentTime -= c.unitedTag.offset);
            else {
                for (var d = 0,
                e = 0; e < s; e++) d += parseInt(c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][e].seconds);
                this.currentTime = d + this.video.currentTime
            }
            this.controls.onTimeUpdate(b);
            this._firstflag || (this._firstflag = !0, this.customWaiting(), this.recordLocalPlayPoint(), this.sendLoadedTime(), n.appendItem("phase", "videotimeupdate"), f.isNeedAdrTrick() && f.adrInvalidPauseCheck(this.video));
            this._comscoreflag || (this._comscoreflag = !0, this._reporter.sendThirdPartyReport("xplayer_h5"));
            this.skipTail(this.currentTime)
        },
        curVideo: function() {
            return this.video
        },
        getQuality: function() {
            if ("m3u8" == c.config.content) {
                var b = this.video.src;
                if ( - 1 !== b.indexOf("mp4")) return "m";
                if ( - 1 !== b.indexOf("flv")) return "f";
                if ( - 1 !== b.indexOf("hd2")) return "h"
            } else return "m"
        },
        bufferedEnd: function() {
            var b = this.curVideo().buffered;
            return 0 == b.length ? 0 : b.end(b.length - 1)
        },
        loadNextVideo: function() {
            var b = c.v.data.videos.next,
            d = this;
            debug.log("loadNextVideo vid = " + b.encodevid);
            if (b.encodevid) {
                var e = {
                    isFullScreen: !0,
                    vid: b.vid,
                    encodevid: b.encodevid,
                    Pt: 2 == window.playmode ? b.seq: null
                };
                c.config.nextAutoPlay = !0;
                l.start(b.encodevid, "", c.config.content,
                function(b, c) {
                    d.startPlay(b, c);
                    try {
                        onPlayerStart(e)
                    } catch(f) {
                        console.log("onPlayerStart error")
                    }
                })
            }
        },
        onPlayEnd: function() {
            f.playerCurrentState = f.playerState.PLAYER_STATE_END;
            debug.log(f.playerCurrentState);
            c.config.events && c.config.events.onPlayEnd && c.v.data.videos ? (debug.log("callback: on play end"), c.config.events.onPlayEnd(c.v.data.videos.next)) : c.config.events && c.config.events.onPlayEnd && (debug.log("callback: on play end"), c.config.events.onPlayEnd())
        },
        onPlayStart: function() {
            c.config.events && c.config.events.onPlayStart && (f.playerCurrentState = f.playerState.PLAYER_STATE_PLAYING, debug.log(f.playerCurrentState), debug.log("callback: on play start"), c.config.events.onPlayStart())
        },
        onMiddleEnded: function() {
            s++;
            this.video.src = c.multiPieceSrc(s);
            this.video.load();
            this.video.play();
            this.video.style.display = "block";
            debug.log("middle src = " + this.video.src)
        },
        onEnded: function(b) {
            if (! (this.isOnePiece() && !0 == this.controls.checkPlayLimit())) if (this.isOnePiece() || s == c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length - 1) y = !0,
            this._reporter.addPlayerDurationReport(61),
            this._reporter.sendTSLog(61),
            this.clearLocalPlayPoint(),
            this.showEndCard(b),
            n.appendItem("phase", "videoended");
            else this.onMiddleEnded(b)
        },
        showEndCard: function(b) {
            this.video.style.display = "none";
            this.controls.onEnded(b);
            this.onPlayEnd()
        },
        onBeginFullscreen: function() {},
        onEndFullscreen: function() {
            if ((f.isIPHONE || f.isIPOD) && null != c.v.data.trial) this.video.style.display = "none"
        },
        detectIsPlaying: function(b) {
            var c = b || 0,
            e = this;
            clearTimeout(this.timeoutTimer);
            0 === this.video.currentTime && 60 >= c && (this.video.load(), this.play(), this.timeoutTimer = setTimeout(function() {
                e.detectIsPlaying(++c)
            },
            1E3))
        },
        isOnePiece: function() {
            return "m3u8" == c.config.content || "mp4" == c.config.content && 1 == c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length
        },
        bindEvent: function() {
            if (!c.v.data.error) if ("directsrc" == c.config.playType && !1 == c.isWeixin) c.addEventHandler(this.video, "play", c.bindAsEventListener(this, this.onPlayIPH)),
            c.addEventHandler(this.video, "timeupdate", c.bindAsEventListener(this, this.onTimeUpdateIPH)),
            c.addEventHandler(this.video, "ended", c.bindAsEventListener(this, this.onEndedIPH)),
            c.addEventHandler(this.video, "webkitendfullscreen", c.bindAsEventListener(this, this.onEndFullscreen));
            else {
                var b = {
                    loadstart: "onLoadStart",
                    canplay: "onCanPlay",
                    loadeddata: "onLoadedData",
                    loadedmetadata: "onLoadedMetaData",
                    abort: "onAbort",
                    error: "onError",
                    pause: "onPause",
                    waiting: "onWaiting",
                    stalled: "onStalled",
                    suspend: "onSuspend",
                    play: "onPlay",
                    volumechange: "onVolumeChange",
                    playing: "onPlaying",
                    seeked: "onSeeked",
                    seeking: "onSeeking",
                    durationchange: "onDurationChange",
                    progress: "onProgress",
                    ratechange: "onRateChange",
                    timeupdate: "onTimeUpdate",
                    ended: "onEnded",
                    webkitbeginfullscreen: "onBeginFullscreen",
                    webkitendfullscreen: "onEndFullscreen"
                },
                d;
                for (d in b) c.addEventHandler(this.video, d, c.bindAsEventListener(this, this[b[d]]))
            }
        }
    };
    var s = -1,
    y = !1,
    ra = 0,
    sa = 600,
    x = {
        flvhd: "\u6807\u6e05",
        flv: "\u6807\u6e05",
        mp4: "\u9ad8\u6e05",
        hd2: "\u8d85\u6e05"
    };
    c.WIN_TYPE = 30;
    c.defaultVideoType = null;
    c.defaultLanguage = "guoyu";
    c.resizeTag = !0;
    c.extend = function(b, c) {
        for (var e in c) b[e] = c[e]
    };
    c.inherits = function(b, c) {
        var e = function() {};
        e.prototype = c.prototype;
        b.prototype = new e;
        b.prototype.constructor = b
    };
    c.bind = function(b, c) {
        return function() {
            return c.apply(b, arguments)
        }
    };
    c.bindAsEventListener = function(b, c) {
        var e = Array.prototype.slice.call(arguments).slice(2);
        return function(g) {
            return c.apply(b, [g || window.event].concat(e))
        }
    };
    c.getCurrentStyle = function(b) {
        return b.currentStyle || document.defaultView.getComputedStyle(b, null)
    };
    c.addEventHandler = function(b, d, e, g) {
        c.config.isMobile && ("click" == d && !g) && (d = "touchend");
        b.addEventListener ? b.addEventListener(d, e, !1) : b.attachEvent ? b.attachEvent("on" + d, e) : b["on" + d] = e
    };
    c.removeEventHandler = function(b, d, e, g) {
        c.config.isMobile && ("click" == d && !g) && (d = "touchend");
        b.removeEventListener ? b.removeEventListener(d, e, !1) : b.detachEvent ? b.detachEvent("on" + d, e) : b["on" + d] = null
    };
    c.show = function(b) {
        b.style.display = "video" === b.tagName.toLowerCase() ? "": "block"
    };
    c.hide = function(b) {
        b && (b.style.display = "none")
    };
    c.getLeftPosition = function(b) {
        for (var c = b.offsetLeft; b.offsetParent;) b = b.offsetParent,
        c += b.offsetLeft;
        return c
    };
    c.get = function(b) {
        return document.querySelector(b)
    };
    c.pieceLength = function() {
        return "m3u8" == c.config.content ? 1 : c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length
    };
    c.multiPieceSrc = function(b) {
        return b >= c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length ? "": c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][b].src
    };
    c.getTime = function(b) {
        if (!b) return "00:00";
        var c = Math.floor(b),
        b = c % 60,
        c = Math.floor(c / 60);
        return (10 > c ? "0" + c: c) + ":" + (10 > b ? "0" + b: b)
    };
    c.addClass = function(b, d) {
        c.hasClass(b, d) || (b.className += " " + d)
    };
    c.hasClass = function(b, c) {
        return RegExp("(^| )" + c + "( |$)").test(b.className)
    };
    c.removeClass = function(b, c) {
        b.className = b.className.replace(RegExp("(^| )" + c + "( |$)"), " ").replace(/^\s+|\s+$/g, "")
    };
    c.m3u8src = function(b, c) {
        var e = "http://v.youku.com/player/getM3U8/vid/" + b + "/type/" + c + "/ts/" + parseInt((new Date).getTime() / 1E3);
        if (f.isIPHONE || f.isIPOD) e += "/useKeyFrame/0";
        return e + "/v.m3u8"
    };
    c.m3u8src_v2 = function(b, d) {
        if (c.OLD_M3U8) return c.m3u8src(b, d);
        var e = {
            vid: b,
            type: d,
            ts: parseInt((new Date).getTime() / 1E3),
            keyframe: f.isIPHONE ? 0 : 1
        };
        c.password && (e.password = c.password);
        c.password && (c.initConfig.client_id && c.config.partner_config && 1 == c.config.partner_config.status && 1 == c.config.partner_config.passless) && (e.client_id = c.initConfig.client_id);
        var g = encodeURIComponent(J(L(M(c.mk.a4 + "poz" + f.userCache.a2, [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), f.userCache.sid + "_" + b + "_" + f.userCache.token)));
        e.ep = g;
        e.sid = f.userCache.sid;
        e.token = f.userCache.token;
        e.ctype = "12";
        e.ev = "1";
        e.oip = c.v.data.security.ip;
        e = "http://pl.youku.com/playlist/m3u8?" + q(e);
        "" != c.getUCStr(b) && (e += c.getUCStr(b));
        return e
    };
    c.isLandScape = function() {
        return 90 == window.orientation || -90 == window.orientation
    };
    c.getUCStr = function(b) {
        var d = "";
        if ("undefined" != typeof getUCSecret) b = getUCSecret(b),
        d += "&xk=" + b;
        else if ("undefined" != typeof uckey) var e = uckey.getUCKey(b),
        d = d + ("&vid=" + b + "&uc_param_str=xk&xk=" + e);
        else ! 0 == c.isUCBrowserAndValidVersion() && (d += "&vid=" + b + "&uc_param_str=xk");
        return d
    };
    c.isUCBrowserAndValidVersion = function() {
        var b = navigator.userAgent,
        c = b.search(/ucbrowser/i);
        return - 1 != c && 9.8 <= parseFloat(b.substr(c + 10, 4)) ? !0 : !1
    };
    var p = function(b) {
        return document.getElementById(b)
    };
    YoukuHTML5Player = function(b, d) {
        null == b.parentBox && (b.parentBox = "parentBox");
        b.expand && 0 < parseInt(b.width) ? (p(b.parentBox).style.width = b.width + "px", p(b.parentBox).style.height = b.height + "px") : (b.width = p(b.parentBox).offsetWidth, b.height = p(b.parentBox).offsetHeight);
        c.config = b;
        var e = p(c.config.parentBox),
        g = parseInt(c.config.width),
        g = '<div id=x-player class="' + D(g) + '">',
        f = "";
        c.isWeixin && (f += "webkit-playsinline");
        if (c.initConfig.iswifi || c.initConfig.autoplay) f += " autoplay";
        e.innerHTML = g + "<video class=x-video-player id=youku-html5player-video  " + f + '></video><div class=x-video-poster><img/></div><div class=x-video-loading></div><div class=x-video-info><h1 class=x-title></h1><div class=x-video-state></div><div class=x-showmore></div><div class=x-mask></div></div><div id=x-video-button class=x-video-button><div class=x-video-play-ico></div></div><div class=x-feedback><div class="x-message"><div class=x-message-txt></div><div class=x-message-btn></div></div><div class="x-mask"></div></div><div class="x-pay"><div class=x-pay-txt><h1><em class=vip></em></h1><p class=x-pay-tips></p></div><div class=x-pay-btn><button type=button id=x-try class=x-btn>\u514d\u8d39\u8bd5\u770b</button><button type=button id=x-pay class="x-btn x-btn-pay"></button></div></div><div class=x-advert><div class=x-advert-info><div class=x-advert-skip><div class=x-advert-txt></div><div class=x-mask></div></div><div class=x-advert-countdown><div class=x-advert-txt></div><div class=x-mask></div></div></div><div class=x-advert-detail><div class=x-advert-txt>\u8be6\u7ec6\u4e86\u89e3<span class=x-ico-detail></span></div><div class=x-mask></div></div></div><div class=x-ad-pause></div><div class=x-prompt></div><div class="x-dashboard"><div class=x-progress-mini><div class=x-progress-track-mini></div><div class=x-progress-load-mini></div><div class=x-progress-play-mini></div></div><div class="x-console"><div class="x-progress"><div class="x-progress-track"><div class="x-progress-load"></div><div class=x-progress-play></div><div class="x-progress-seek"><div class="x-seek-handle"></div></div></div></div><div class="x-controls"><div class="x-play-control"><button class="x-control-btn"><b id=x-playbtn class="x-playing"><em>\u64ad\u653e</em></b></button></div><div class="x-time-display"><span class="x-time-current">00:00</span><span class="x-time-splite">/</span><span class="x-time-duration">00:00</span></div><div class="x-settings"><div class=x-playspeed></div><div class=x-playshow style=display:none><button class=x-control-btn title=\u9009\u96c6>\u9009\u96c6</button></div><div class="x-localization"></div><div class="x-quality"></div><div class="x-fullscreen"><button class="x-control-btn" type="button" title="\u5168\u5c4f\u6a21\u5f0f" rol="button"><b class=x-zoomin><em>\u5168\u5c4f</em></b></button></div></div></div></div></div><div class=x-showlist></div><div class=x-tips></div><div class=x-trigger></div></div>';
        Y.apply(this, arguments);
        this.video.style.width = "100%";
        this.video.style.height = "100%";
        this.video.style.display = "none";
        this.video.style.position = "relative";
        this._firstPlayTag = !1;
        this._retry = 2;
        this.uiAdapter()
    };
    c.inherits(YoukuHTML5Player, Y);
    c.extend(YoukuHTML5Player.prototype, {
        startPlay: function(b, d, e) {
            if (b && b.data && (b.data.show = b.data.show || {},
            d.abstarttime = (new Date).getTime(), d._playListData = b.data, d._user = b.user, c.v = b, c.videoInfo = d, this.setting = {},
            c.extend(this.setting, e), !b.data.error || !this.processError(b, d, e))) if (this._reporter = new V(this, c.v, c.videoInfo._sid), this.controls = this.setupControls(this), this.controls.init(c.v, c.videoInfo), this.mpieceReport(), this.createIdNode(), this.isNeedAdRequest()) this.processAd();
            else if (this.controls.bindVideoBtnEvent(), this.realStartPlay(), 1 == c.initConfig.ucautoplay) this.controls.onVideoBtnClick({})
        },
        isNeedAdRequest: function() {
            "undefined" == typeof this._frontAdTag && (this._frontAdTag = !1);
            f.isNeedFrontAd = !this._frontAdTag && "directsrc" != c.config.playType && !c.v.data.trial;
            return f.isNeedFrontAd
        },
        processAd: function() {
            if (this.isNeedAdRequest() && (this._frontAdTag = !0, this._adplugin = new X(this, c.v, c.videoInfo._sid), this.bind_frontAd = c.bindAsEventListener(this, this.onFrontAdInfoOK), this.bind_frontAdInfoTimeout = c.bindAsEventListener(this, this.onFrontAdInfoTimeout), this._adplugin.addEventListener("frontAdinfook", this.bind_frontAd, !1), this._adplugin.addEventListener("frontAdinfotimeout", this.bind_frontAdInfoTimeout), this.bind_unitedFrontAd = c.bindAsEventListener(this, this.onUnitedFrontAdInfoOK), this._adplugin.addEventListener("unitedfrontadinfook", this.bind_unitedFrontAd, !1), this.bind_backAdInfoOK = c.bindAsEventListener(this, this.onBackAdInfoOK), this.bind_backAdInfoTimeout = c.bindAsEventListener(this, this.onBackAdInfoTimeout), this._adplugin.addEventListener("backAdinfook", this.bind_backAdInfoOK, !1), this._adplugin.addEventListener(" backAdinfotimeout", this.bind_backAdInfoTimeout), this.bind_uglyCloseAd = c.bindAsEventListener(this, this.onUglyCloseAd), this._adplugin.addEventListener("uglyclosead", this.bind_uglyCloseAd), this.controls.bindAdVideoBtnEvent(), window.adpluginobject = this._adplugin, 1 == c.initConfig.ucautoplay)) this.controls.onVideoBtnTouchEnd({})
        },
        requestAd: function() {
            this._adplugin && this._adplugin.frontAd()
        },
        onUglyCloseHint: function() {
            this.controls.showUglyHint()
        },
        onUglyCloseAd: function() {
            debug.log("ugly close");
            this.controls.closeUglyHint();
            this.adplayer.uglyClose()
        },
        onFrontAdInfoTimeout: function() {
            this._hasStartPlay = !0;
            this.realStartPlay(!0)
        },
        onUnitedFrontAdInfoOK: function(b) {
            debug.log("<b>on united front adinfo ok</b>");
            var d = b.data.info;
            if (0 == b.data.info.VAL.length) debug.log("<b>onUnitedFrontAdInfoOK val length == 0 </b>"),
            this.loadVTVC(b.data.vtvc),
            this.video.src = c.m3u8src_v2(c.v.data.id, c.defaultVideoType),
            this.unitedStartPlay(d, !0);
            else {
                this.adplayer = new za(this, b);
                var e = this;
                this.adplayer.addEventListener(B,
                function() {
                    debug.log("<font color=red>united ad end</font>");
                    e._realFlag || (e._realFlag = !0, e.adplayer.clearTimer(), e.unitedStartPlay(d))
                },
                !1);
                this.adplayer.addEventListener(z,
                function() {
                    debug.log("<font color=red>united ad error</font>");
                    e._realFlag || (c.unitedTag = null, e._realFlag = !0, e.adplayer.clearTimer(), e.video.src = c.m3u8src_v2(c.v.data.id, c.defaultVideoType), e.unitedStartPlay(d, !0))
                },
                !1);
                this.adplayer.addEventListener(G,
                function() {
                    debug.log("<b>ugly hint</b>");
                    e.onUglyCloseHint()
                },
                !1);
                this.adplayer.play();
                this.createIdNode()
            }
        },
        loadVTVC: function(b) {
            for (var c = 0; c < b.length; c++) C(b[c].VC, "js")
        },
        onFrontAdInfoOK: function(b) {
            debug.log("onFrontAdInfoOK");
            if (!0 !== this._hasStartPlay) if (0 == b.data.urls.length) this.loadVTVC(b.data.vtvc),
            this.realStartPlay(!0);
            else {
                f.playerCurrentState = f.playerState.PLAYER_STATE_AD;
                debug.log(f.playerCurrentState);
                this.adplayer = new W(this, b);
                var c = this;
                this.adplayer.addEventListener(B,
                function(b) {
                    debug.log("ad end");
                    c._realFlag || (c._realFlag = !0, c.adplayer.clearTimer(), c.realStartPlay(b.data))
                },
                !1);
                this.adplayer.addEventListener(z,
                function(b) {
                    debug.log("<font color=red>ad error</font>");
                    c._realFlag || (c._realFlag = !0, c.adplayer.clearTimer(), c.realStartPlay(b.data))
                },
                !1);
                this.adplayer.addEventListener(G,
                function() {
                    debug.log("<b>ugly hint</b>");
                    c.onUglyCloseHint()
                },
                !1);
                this.adplayer.play();
                this.createIdNode()
            }
        },
        onBackAdInfoTimeout: function() {
            debug.log("onBackAdInfoTimeout");
            this.showEndCard()
        },
        onBackAdInfoOK: function(b) {
            debug.log("onBackAdInfoOK");
            if (0 == b.data.urls.length) this.showEndCard();
            else {
                this.adplayer = new W(this, b);
                var c = this;
                this.adplayer.addEventListener(B,
                function() {
                    c.showEndCard()
                });
                this.adplayer.addEventListener(z,
                function() {
                    c.showEndCard()
                });
                this.adplayer.play()
            }
        },
        prepareVideoTag: function() {
            this.video.preload = "none";
            "m3u8" == c.config.content ? this.video.src = c.videoInfo.src: null != c.videoInfo._videoSegsDic && null != c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType] && (this.video.src = c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][0].src);
            c.v.data.trial && ("episodes" != c.v.data.trial.type && 0 == c.v.data.trial.time) && (this.video.src = null);
            this.createIdNode()
        },
        createIdNode: function() {
            if (!p(c.config.id)) {
                var b = document.createElement("div");
                b.id = c.config.id;
                p(c.config.parentBox).appendChild(b)
            }
        },
        redirect: function() {
            var b = "";
            "m3u8" == c.config.content ? b = c.videoInfo.src: null != c.videoInfo._videoSegsDic && null != c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType] && (b = c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][0].src);
            debug.log("redirect play src=" + b);
            this._reporter.addPlayerStaticReport();
            this._reporter.addPlayerDurationReport(59);
            this._reporter.sendVVLog(59);
            this._reporter.sendTSLog(60);
            this._reporter.sendUserActionReport("xps", "c");
            window.open(b, "", "", !1);
            this._reporter.sendClientConsumeReport();
            this.onPlayStart()
        },
        realStartPlay: function(b) {
            debug.log("realStartPlay " + b);
            this.controls.bindEvent();
            this.bindEvent();
            this.prepareVideoTag();
            this.playVideos(b)
        },
        unitedStartPlay: function(b, d) {
            debug.log("<b>united start play </b>");
            c.unitedTag = {
                offset: b.VAL.length ? b.VAL[0].AL: 0
            };
            this.controls.bindEvent();
            this.bindEvent();
            if (!0 === d) this.video.load(),
            this.video.play();
            else this.onPlay();
            this.controls.onPlay()
        },
        playVideos: function(b) {
            debug.log("playVideos " + b);
            y = !1;
            s = 0;
            this.video.style.display = (f.isIPHONE || f.isIPOD) && null != c.v.data.trial ? "none": "block";
            if (c.config.autoplay || c.config.nextAutoPlay || b) debug.log("src= " + this.video.src + " auto = " + b),
            this.video.load(),
            this.video.play()
        },
        processError: function(b) {
            if ( - 301 == b.data.error.code) return b.data.trial = {
                time: 0
            },
            !1;
            c.hide(c.get(".x-video-poster"));
            this.feedbackPanel = new U(this, b);
            return ! 0
        },
        mpieceReport: function() {
            "mp4" == c.config.content && (c.videoInfo._videoSegsDic && null != c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType] && 1 < c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length) && (debug.log("mpiece report"), f.Log(f.MPIECEURL + u({
                partner: c.config.partnerId,
                type: c.defaultVideoType,
                length: c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length,
                vid: c.v.data.id
            })))
        },
        resize_: function(b, d, e) {
            debug.log("resize=" + c.resizeTag);
            d && (e && c.resizeTag && this.controls) && (b = this.controls.xplayer.className, this.controls && this.controls.xplayer && ( - 1 === b.indexOf("fullscreen") ? this.controls.xplayer.className = D(d) : (d = window.innerWidth, this.controls.xplayer.className = D(d) + " x-player-fullscreen")))
        },
        uiAdapter: function() {
            "index" == c.config.wintype && (c.hide(c.get(".x-localization")), c.hide(c.get(".x-quality")));
            c.get("#x-video-button").className = "x-video-button";
            "m3u8" != c.config.content && c.hide(c.get(".x-quality"));
            var b = this;
            window.addEventListener("resize",
            function(c) {
                debug.log("window.resize");
                if (b.controls) b.controls.onResize(c)
            },
            !1)
        },
        isOutTryDuration: function(b) {
            return this.tryDuration ? b >= this.tryDuration: !1
        },
        replay: function() {
            s = 0;
            this._ireflag = this._comscoreflag = !1;
            this._firstflag = f.adrPlayTrick = !1;
            this.video.style.display = "block";
            this.isOnePiece() || (this.video.src = c.multiPieceSrc(s));
            f.isIPAD && (this.video.src = c.m3u8src_v2(c.v.data.id, c.defaultVideoType), c.unitedTag = null);
            this.video.load();
            this.video.play();
            this._reporter.tsInit();
            this._reporter.sendVVLog(62);
            this._reporter.sendTSLog(60);
            this._reporter.addPlayerDurationReport(62)
        },
        seekToLastPoint: function() {
            if (f.isAndroid) return ! 1;
            var b = c.v.data.id,
            d = -1;
            c.v.data.playlog && (d = c.v.data.playlog.lastpoint / 1E3);
            var e = parseInt(n.getItem(b + "_playpoint")) || -1,
            b = -1; - 1 != d && -1 != e ? (b = d, 60 > Math.abs(d - e) && (b = e)) : (b = d, -1 == d && (b = e));
            debug.log("lastpoint=" + b);
            d = n.getItem("youku_ignore_lasttime");
            d = parseInt(d) || 0;
            return - 1 !== b && 120 <= b && 3 > d && !c.v.data.trial && b < c.videoInfo.totalTime - 120 ? (this.controls.showLastTimeTip(b), f.isAndroid && (this._waitSeek = b), this.seek(b), !0) : !1
        },
        clearLocalPlayPoint: function() {
            var b = c.v.data.id;
            clearTimeout(this._recordLPPTimer);
            n.removeItem(b + "_playpoint")
        },
        recordLocalPlayPoint: function() {
            var b = c.v.data.id + "",
            d = this.currentTime || 0,
            e = this;
            this._recordLPPTimer = setTimeout(function() {
                e.recordLocalPlayPoint()
            },
            1E4);
            n.removeItem(b + "_playpoint");
            if (600 <= c.v.data.video.seconds && (d < c.videoInfo.totalTime - 120 && !c.v.data.trial && 120 <= d) && (n.setItem(b + "_playpoint", d), !this.updatePPVids)) {
                this.updatePPVids = !0;
                d = n.getItem("youku_playpoint_vids") || "";
                if ("" == d) d = b;
                else {
                    for (var d = d.split(":"), g = 0; g < d.length; g++) d[g] == b && (d[g] = "");
                    d.push(b);
                    d = d.join(":");
                    for (b = 0;
                    ":" == d.charAt(b);) b++;
                    d = d.substring(b);
                    d = d.replace(/:(:)+/g, ":")
                }
                b = d.split(":");
                30 < b.length && (debug.log("slice"), n.removeItem(b[0] + "_playpoint"), d = b.slice(1).join(":"));
                debug.log("youku_playpoint_vids=" + d);
                n.setItem("youku_playpoint_vids", d)
            }
        },
        skipHead: function() {
            if (!f.isAndroid) {
                var b = parseInt((c.v.data.dvd || {}).head || -1);
                debug.log("skiphead = " + b); - 1 != b && (this.controls.tipPanel.onSkipHead(), "true" == n.getItem("youku_conf_skip") && (f.isAndroid && (this._waitSeek = b / 1E3), this.seek(b / 1E3)))
            }
        },
        skipTail: function(b) {
            if (!f.isAndroid) {
                var d = parseInt((c.v.data.dvd || {}).tail || -1); - 1 != d && (b >= d / 1E3 - 10 && !this._tailTip) && (debug.log("skiptail(act before 10) =" + d), this._tailTip = !0, this.controls.tipPanel.onSkipTail()); - 1 != d && (b >= d / 1E3 && !this._tailSkipped) && (this._tailSkipped = !0, "true" == n.getItem("youku_conf_skip") && this.seek(parseInt(c.v.data.video.seconds) - 1))
            }
        },
        assistSkipTail: function(b) {
            var d = parseInt((c.v.data.dvd || {}).tail || -1);
            this._tailTip = b >= d / 1E3 ? this._tailSkipped = !0 : this._tailSkipped = !1
        },
        seek: function(b, d) {
            b = b || 0;
            b = Math.max(b, 0);
            c.videoInfo.totalTime && (b = Math.min(b, c.videoInfo.totalTime - 5));
            this.isOutTryDuration(b) && (b = this.tryDuration - 1);
            this.assistSkipTail(b);
            var e = this;
            this.switchTimer && clearTimeout(this.switchTimer);
            this.currentTime = b;
            if (this.isOnePiece()) {
                var g = this.video.seekable,
                f = g.end(0);
                c.unitedTag && (b += c.unitedTag.offset, f = g.end(0) + c.unitedTag.offset);
                1 == g.length && b < f ? (debug.log("seek ct = " + b + ",end = " + g.end(0)), this.seekTo(b, d)) : (this.controls.onWaiting(), this.switchTimer = setTimeout(function() {
                    e.seek(b, d)
                },
                100))
            } else debug.log("multi seek"),
            this.multiSeekTo(b)
        },
        seekTo: function(b, c) {
            if (this.isOnePiece()) {
                debug.log("is one piece");
                var e = this;
                try {
                    e.video.currentTime = b
                } catch(g) {
                    var f = 0;
                    this.video.addEventListener("canplay",
                    function() {
                        1 !== f && (f = 1, debug.log("canplay time=" + b), e.video.currentTime = b)
                    })
                }
                "function" == typeof c && (debug.log("<b>seekto callback(mayby play)</b>"), c())
            }
        },
        multiSeekTo_: function() {
            debug.log("YoukuHTML5 ")
        },
        multiSeekTo: function(b) {
            debug.log("YoukuHTML5Player multiSeekTo !");
            for (var d = 0,
            e = 0,
            g = 0,
            f = 0; f < c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType].length; f++) {
                var h = parseInt(c.videoInfo._videoSegsDic.streams[c.defaultLanguage][c.defaultVideoType][f].seconds),
                d = d + h;
                if (d > b) {
                    e = f;
                    g = h - (d - b);
                    break
                } else if (d == b) {
                    e = f + 1;
                    g = 0;
                    break
                }
            }
            this.video.pause();
            if (e == s) {
                debug.log(" piece time = " + g);
                try {
                    this.video.currentTime = g
                } catch(j) {}
                this.video.play()
            } else {
                s = e;
                var l = 0,
                n = this;
                this.video.addEventListener("canplay",
                function() {
                    1 !== l && (l = 1, debug.log("canplay time=" + g), n.video.currentTime = g)
                }); (b = c.multiPieceSrc(s)) ? (this.video.src = b, this.video.load(), this.video.play()) : this.video.pause()
            }
            this.video.style.display = "block"
        },
        adjustVideoRatio: function(b) {
            if (!f.isIOS) {
                if (("onorientationchange" in window || "orientation" in window) && !this._avrTag) {
                    this._avrTag = !0;
                    var d = this;
                    window.addEventListener("orientationchange",
                    function() { ! 0 === d.controls.fullscreenPanel.fullFlag() && d.adjustVideoRatio()
                    })
                }
                var d = this,
                e = this.video;
                setTimeout(function() {
                    if (1 === b) e.style.width = "100%",
                    e.style.height = "100%",
                    e.style.top = null,
                    e.style.left = null;
                    else {
                        var d = c.get(".x-player"),
                        d = d.offsetWidth / d.offsetHeight,
                        f = e.videoWidth / e.videoHeight;
                        isNaN(f) || isNaN(d) || !isFinite(d) || !isFinite(f) ? (e.style.width = "100%", e.style.height = "100%", e.style.top = null, e.style.left = null) : d < f ? (e.style.width = "100%", e.style.height = 100 * (d / f) + "%", e.style.top = 100 * (1 / d - 1 / f) / 2 * d + "%", e.style.left = null) : (e.style.height = "100%", e.style.width = 100 * (f / d) + "%", e.style.left = 100 * ((d - f) / 2 / d) + "%", e.style.top = null)
                    }
                },
                2E3)
            }
        }
    });
    window.YoukuPlayerSelect = T;
    window.BuildVideoInfo = l;
    window.checkSrc = function() {
        l._fyks.length > l.mp4srcs.length || (clearInterval(l._tid), l.cleanSrc(), l.cache(), null == l._callback ? f.GetMP4OK(l._v, l._videoInfo) : l._callback(l._v, l._videoInfo))
    };
    window.QS = function() {
        var b = {},
        c = window.location.search.match(RegExp("[?&][^?&]+=[^?&]+", "g"));
        if (null != c) for (var e = 0; e < c.length; e++) {
            var f = c[e],
            i = f.indexOf("="),
            h = f.substring(1, i),
            f = f.substring(i + 1);
            "true" == f ? f = !0 : "false" == f || isNaN(f) || (f = +f);
            "undefined" == typeof b[h] ? b[h] = f: b[h] instanceof Array ? b[h].push(f) : b[h] = [b[h], f]
        }
        return b
    };
    window.YKP = f;
    window.YKU = H;
    window.YoukuHTML5Player = YoukuHTML5Player;
    for (var Z = document.getElementsByTagName("script"), O = 0; O < Z.length; O++) if ( - 1 !== Z[O].src.indexOf("player.youku.com/jsapi")) {
        eval(Z[O].innerHTML);
        break
    }
    window.notifyYKU = function() {
        H.swfLoaded = 1
    };
    window.onPlayerStart = function() {
        c.initConfig.events && c.initConfig.events.onPlayStart && (f.playerCurrentState = f.playerState.PLAYER_STATE_PLAYING, debug.log(f.playerCurrentState), debug.log("api:flash play start"), c.initConfig.events.onPlayStart())
    };
    window.onPlayerComplete = function() {
        c.initConfig.events && c.initConfig.events.onPlayEnd && (f.playerCurrentState = f.playerState.PLAYER_STATE_END, debug.log(f.playerCurrentState), debug.log("api:flash play end"), c.initConfig.events.onPlayEnd())
    }
})();