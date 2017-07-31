window.convodump = {
    rewrite_candidates: function(e){
	let l=[];
	let helper=function(e){
	    let cs=e.children;
	    let n=cs.length;
	    for (let i=0; i<n; i++) {
		c=cs[i];
		href=c.getAttribute('href');
		src=c.getAttribute('src');
		if (href!=null || src!=null) {
		    l.push({
			tag: c.tagName,
			href: href,
			src: src
		    });
		}
		helper(c);
	    };
	};
	helper(e);
	return l;
    },

    rewrite_from_list:function(e,l){
	let N=0;
	let helper=function(e){
	    let cs=e.children;
	    let n=cs.length;
	    for (let i=0; i<n; i++) {
		c=cs[i];
		href=c.getAttribute('href');
		src=c.getAttribute('src');
		if (href!=null || src!=null) {
		    c.setAttribute('href',l[N].href || href);
		    c.setAttribute('src',l[N].src || src);
		}
		N++;
		helper(c);
	    };
	};
    }
};

//let messages=document.getElementById('messageGroup').children[1];
