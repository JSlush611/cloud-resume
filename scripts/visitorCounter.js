document.addEventListener('DOMContentLoaded', async function () {
    try {
        await getVisitorCount();

        let uniqueId = getCookie('uniqueId');
        const fingerprint = await getFingerprint();

        const visitorData = await checkVisitorData(fingerprint, uniqueId);
        if (!visitorData.exists) {
            await incrementVisitorCount();

            uniqueId = uniqueId || generateUniqueId();
            setCookie('uniqueId', uniqueId, 365);

            await addVisitor(uniqueId, fingerprint);
        } else if (!uniqueId) {
            setCookie('uniqueId', visitorData.cookie, 365);
        }
    } catch (error) {
        console.error('Error during DOMContentLoaded:', error);
    }
});

async function getFingerprint() {
    const FingerprintJS = await import('https://openfpcdn.io/fingerprintjs/v4')
        .then(FingerprintJS => FingerprintJS.load());
    const result = await FingerprintJS.get();
    return result.visitorId;
}

function generateUniqueId() {
    return 'uid_' + Math.random().toString(36).substr(2, 9);
}

async function checkVisitorData(fingerprint, uniqueId) {
    const response = await fetch('https://us-central1-cloud-resume-407121.cloudfunctions.net/check_visitor_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fingerprint, uniqueId })
    });
    return await response.json();
}

async function incrementVisitorCount() {
    const response = await fetch('https://us-central1-cloud-resume-407121.cloudfunctions.net/increment_visitor_count', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    const data = await response.json();
    updateVisitorCount(data.updated_count); 
}

async function getVisitorCount() {
    const response = await fetch('https://us-central1-cloud-resume-407121.cloudfunctions.net/get_visitor_count', {
        method: 'GET', 
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    updateVisitorCount(data.counter_value);
}

async function addVisitor(cookie, fingerprint) {
    await fetch('https://us-central1-cloud-resume-407121.cloudfunctions.net/add_visitor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cookie, fingerprint })
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function updateVisitorCount(newCount) {
    const visitorCountElement = document.getElementById('visitor-count');
    if (visitorCountElement) {
        visitorCountElement.textContent = newCount;
    }
}