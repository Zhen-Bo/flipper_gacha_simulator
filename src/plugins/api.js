let baseURL = process.env.VUE_APP_HOST_NAME || '';

export default {
  /**
   * @param {string} pool
   * @returns {Promise<{data:Array<{attri: string, id: string, name: string, rarity:string}>, total:number, report: {all_five: number, all_four: number, all_roll: number, all_three: number}}>}
   */
  roll (pool) {
    return fetch(`${baseURL}/wf/roll?pool=${pool}`)
      .then(res => res.json());
  },
  report (pool) {
    return fetch(`${baseURL}/wf/result?pool=${pool}&data_mode=true`)
      .then(res => res.json());
  }
};