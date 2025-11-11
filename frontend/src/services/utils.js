export const formatCost = (cost) => {
    return `$${cost.toFixed(4)}`;
  };
  
  export const formatNumber = (num) => {
    return num.toLocaleString();
  };
  
  export const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };
  
  export const parseAgentName = (agentName) => {
    return agentName
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };