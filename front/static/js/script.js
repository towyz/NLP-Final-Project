document.addEventListener('DOMContentLoaded', function() {
    // 加载热搜列表
    fetchTrendingList();
    // 加载推荐列表
    fetchRecommandedList();
    
    // 搜索表单提交
    document.getElementById('searchForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const query = document.getElementById('searchInput').value.trim();
        if (query) {
            performSearch(query);
        }
    });
});

function fetchTrendingList() {
    fetch('/api/trending')
        .then(response => response.json())
        .then(data => {
            const trendingList = document.getElementById('trendingList');
            trendingList.innerHTML = '';
            
            data.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <a href="${item.url}" target="_blank">${item.topic}</a>
                    <span class="hotness">(${item.hotness})</span>
                `;
                li.addEventListener('click', function(e) {
                    e.preventDefault();
                    // document.getElementById('searchInput').value = item.topic;
                    // performSearch(item.topic);
                    // 改为了 进入 url，不然要写太多了
                    window.location.href = item.url;
                });
                trendingList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching trending list:', error));
}

function fetchRecommandedList() {
    fetch('/api/get_recommendations').then(response => response.json()).then(data => {
        const recommendList = document.getElementById('recommendList');
        recommendList.innerHTML = '';

        data.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${item.url}" target="_blank">${item.topic}</a>
            `;
            li.addEventListener('click', function(e) {
                e.preventDefault();
                // document.getElementById('searchInput').value = item.topic;
                window.location.href = item.url;
            });
            recommendList.appendChild(li);
        });
    }).catch(error => console.error('Error fetching recommandation list:', error));
}

function performSearch(query) {
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('searchResults').innerHTML = 
            '<p>搜索过程中发生错误，请稍后再试。</p>';
    });
}

function displayResults(results) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>没有找到相关结果。</p>';
        return;
    }
    
    let html = '<div class="result-header">';
    html += `<p>找到约 ${results.length} 条结果</p>`;
    html += '</div>';
    
    results.forEach(result => {
        html += `<div class="result-item">
            <h3><a href="${result.url}" target="_blank">${result.title}</a></h3>
            <p class="url">${result.url}</p>
            <p class="snippet">${result.snippet}</p>
        </div>`;
    });
    
    resultsContainer.innerHTML = html;
}