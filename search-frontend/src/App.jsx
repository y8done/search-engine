import { useState } from 'react'
import './App.css'
function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    setIsSearching(true);

    try {
      const response = await fetch(`http://localhost:5000/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      setIsSearching(false);
    }
  }

  return (
    // min-h-screen ensures it covers the whole vertical height
    <div className="min-h-screen bg-black text-white px-5 py-12 font-sans">
      
      {/* Centered container wrapper */}
      <div className="max-w-3xl mx-auto">
        
        <h1 className="text-center text-4xl font-bold tracking-widest text-white mb-8">
          WikiLook
        </h1>
        
        <form onSubmit={handleSearch} className="flex gap-3 mb-10">
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Wikipedia..." 
            // focus:outline-none focus:ring stops the default ugly browser outline and adds a slick glow
            className="flex-1 px-5 py-3 text-base rounded-full border border-gray-700 bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
          />
          <button 
            type="submit" 
            className="px-6 py-3 text-base font-bold rounded-full bg-white text-black hover:bg-gray-200 transition-colors cursor-pointer"
          >
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </form>

        {/* The Results Container */}
        <div className="flex flex-col gap-4">
          {results.length > 0 ? (
            results.map((item, index) => (
              <div 
                key={index} 
                className="p-5 border border-gray-800 rounded-lg bg-gray-900 hover:border-gray-600 transition-colors"
              >
                <a 
                  href={item.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  // break-all prevents massive URLs from breaking out of the box
                  className="text-lg font-bold text-blue-400 hover:text-blue-300 hover:underline break-all"
                >
                  {item.url}
                </a>
                <p className="mt-2 text-sm text-gray-400">
                  TF-IDF Relevance Score: <span className="text-gray-300 font-mono">{item.score}</span>
                </p>
              </div>
            ))
          ) : (
            <p className="text-center text-gray-500 mt-10">No results to display.</p>
          )}
        </div>

      </div>
    </div>
  )
}

export default App