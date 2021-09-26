let baseURL = process.env.VUE_APP_HOST_NAME || '';
let resourceURL = process.env.VUE_APP_RESOURCE_URL || '';

/** @typedef  {Object} character
 * @property {string} attri
 * @property {string} id
 * @property {string} name
 * @property {'5-up','5','4','3'} rarity
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
  report (pool) {
    return fetch(`${baseURL}/wf/result?pool=${pool}&data_mode=true`)
      .then(res => res.json());
  },
  pool(){
    return fetch(`${baseURL}/wf/result?get_pool=true`)
      .then(res => res.json());
  }
};
