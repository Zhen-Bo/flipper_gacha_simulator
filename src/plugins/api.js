let baseURL = process.env.VUE_APP_HOST_NAME || '';
let resourceURL = process.env.VUE_APP_RESOURCE_URL || '';

/** @typedef  {Object} character
 * @property {string} attri
 * @property {string} id
 * @property {string} name
 * @property {'5-pu','5','4','3'} rarity
 * */

export default {
  resourceURL,
  /**
   * @param {string} pool
   * @returns {Promise<{data:Array<character>, total:number, report: {all_five: number, all_four: number, all_roll: number, all_three: number}}>}
   */
  roll (pool) {
    return fetch(`${baseURL}/wf/roll?pool=${pool}`)
      .then(res => res.json());
  },
  /**
   * @param {string} pool
   * @returns {Promise<{all_five: number, all_four: number, all_roll: number, all_three: number}>}
   */
  report (pool) {
    return fetch(`${baseURL}/wf/result/roll_data?pool=${pool}`)
      .then(res => res.json());
  },
  search(pool, num){
    return fetch(`${baseURL}/wf/result?pool=${pool}&roll=${num}`)
      .then(res => res.json());
  },
  pool(){
    return fetch(`${baseURL}/wf/result?get_pool=true`)
      .then(res => res.json());
  },
  getZoom(width){
    console.log(width);
    switch (true){
      case width === 600:
        return 1.5;
    }
  },
  round(num){
    return (Math.round(num * 10000) / 100).toFixed(2);
  }
};
